"use client"


import type React from "react"
import { useState, useRef, useEffect } from "react"
import {
  Search,
  Plus,
  Lightbulb,
  ArrowUp,
  Menu,
  PenSquare,
  RefreshCcw,
  Copy,
  Share2,
  ThumbsUp,
  ThumbsDown,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { cn } from "@/lib/utils"
import { ModeToggle } from "@/components/DarkMode";
// import { useToast } from "@/components/ui/sonner"
import { toast } from "sonner"
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

type ActiveButton = "none" | "add" | "deepSearch" | "think"
type MessageType = "user" | "system"

interface Message {
  id: string
  content: string
  type: MessageType
  completed?: boolean
  newSection?: boolean
}

interface MessageSection {
  id: string
  messages: Message[]
  isNewSection: boolean
  isActive?: boolean
  sectionIndex: number
}

interface StreamingWord {
  id: number
  text: string
}

interface Metadata {
  categories: string[]
  created_by: string
  github_link: string
  language: string
  link: string
  stars: string
  title: string
}

interface AIResponse {
  message: string
  metadata: Metadata
}

// Faster word delay for smoother streaming
const WORD_DELAY = 40 // ms per word
const CHUNK_SIZE = 2 // Number of words to add at once

export default function ChatInterface() {
  // const { toast } = useToast()
  const [inputValue, setInputValue] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const chatContainerRef = useRef<HTMLDivElement>(null)
  const newSectionRef = useRef<HTMLDivElement>(null)
  const [hasTyped, setHasTyped] = useState(false)
  const [activeButton, setActiveButton] = useState<ActiveButton>("none")
  const [isMobile, setIsMobile] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [messageSections, setMessageSections] = useState<MessageSection[]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const [streamingWords, setStreamingWords] = useState<StreamingWord[]>([])
  const [streamingMessageId, setStreamingMessageId] = useState<string | null>(null)
  const [viewportHeight, setViewportHeight] = useState(0)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [completedMessages, setCompletedMessages] = useState<Set<string>>(new Set())
  const [activeSectionId, setActiveSectionId] = useState<string | null>(null)
  const inputContainerRef = useRef<HTMLDivElement>(null)
  const shouldFocusAfterStreamingRef = useRef(false)
  const mainContainerRef = useRef<HTMLDivElement>(null)
  // Store selection state
  const selectionStateRef = useRef<{ start: number | null; end: number | null }>({ start: null, end: null })
  const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

  // Constants for layout calculations to account for the padding values
  const HEADER_HEIGHT = 48 // 12px height + padding
  const INPUT_AREA_HEIGHT = 100 // Approximate height of input area with padding
  const TOP_PADDING = 48 // pt-12 (3rem = 48px)
  const BOTTOM_PADDING = 128 // pb-32 (8rem = 128px)
  const ADDITIONAL_OFFSET = 16 // Reduced offset for fine-tuning

  const checkBackendServerRunning = async () => {
    let attempts = 0;
    const maxAttempts = 40;
    
    const tryConnect = async () => {
      try {
        const response = await fetch(`${BASE_URL}`, {
          method: "GET",
          headers: {
            "accept": "application/json"
          },
        });
        
        if (!response.ok) {
          throw new Error(`Backend server error: ${response.status} ${response.statusText}`);
        }
        toast.success('Connected to backend server');
        return true;
      } catch (error) {
        attempts++;
        if (attempts >= maxAttempts) {
          if (error instanceof TypeError && error.message.includes('fetch')) {
            toast.error('Cannot connect to backend server after 40 seconds. Please ensure it is running.');
          } else {
            toast.error('Unexpected error connecting to backend');
          }
          console.error('Backend connection error:', error);
          return false;
        }
        await new Promise(resolve => setTimeout(resolve, 1000));
        return tryConnect();
      }
    };
  
    await tryConnect();
  }

  useEffect(() => {
    checkBackendServerRunning();
  }, [])

  // Check if device is mobile and get viewport height
  useEffect(() => {
    const checkMobileAndViewport = () => {
      const isMobileDevice = window.innerWidth < 768
      setIsMobile(isMobileDevice)

      // Capture the viewport height
      const vh = window.innerHeight
      setViewportHeight(vh)

      // Apply fixed height to main container on mobile
      if (isMobileDevice && mainContainerRef.current) {
        mainContainerRef.current.style.height = `${vh}px`
      }
    }

    checkMobileAndViewport()

    // Set initial height
    if (mainContainerRef.current) {
      mainContainerRef.current.style.height = isMobile ? `${viewportHeight}px` : "100svh"
    }

    // Update on resize
    window.addEventListener("resize", checkMobileAndViewport)

    return () => {
      window.removeEventListener("resize", checkMobileAndViewport)
    }
  }, [isMobile, viewportHeight])

  // Organize messages into sections
  useEffect(() => {
    if (messages.length === 0) {
      setMessageSections([])
      setActiveSectionId(null)
      return
    }

    const sections: MessageSection[] = []
    let currentSection: MessageSection = {
      id: `section-${Date.now()}-0`,
      messages: [],
      isNewSection: false,
      sectionIndex: 0,
    }

    messages.forEach((message) => {
      if (message.newSection) {
        // Start a new section
        if (currentSection.messages.length > 0) {
          // Mark previous section as inactive
          sections.push({
            ...currentSection,
            isActive: false,
          })
        }

        // Create new active section
        const newSectionId = `section-${Date.now()}-${sections.length}`
        currentSection = {
          id: newSectionId,
          messages: [message],
          isNewSection: true,
          isActive: true,
          sectionIndex: sections.length,
        }

        // Update active section ID
        setActiveSectionId(newSectionId)
      } else {
        // Add to current section
        currentSection.messages.push(message)
      }
    })

    // Add the last section if it has messages
    if (currentSection.messages.length > 0) {
      sections.push(currentSection)
    }

    setMessageSections(sections)
  }, [messages])

  // Scroll to maximum position when new section is created, but only for sections after the first
  useEffect(() => {
    if (messageSections.length > 1) {
      setTimeout(() => {
        const scrollContainer = chatContainerRef.current

        if (scrollContainer) {
          // Scroll to maximum possible position
          scrollContainer.scrollTo({
            top: scrollContainer.scrollHeight,
            behavior: "smooth",
          })
        }
      }, 100)
    }
  }, [messageSections])

  // Focus the textarea on component mount (only on desktop)
  useEffect(() => {
    if (textareaRef.current && !isMobile) {
      textareaRef.current.focus()
    }
  }, [isMobile])

  // Set focus back to textarea after streaming ends (only on desktop)
  useEffect(() => {
    if (!isStreaming && shouldFocusAfterStreamingRef.current && !isMobile) {
      focusTextarea()
      shouldFocusAfterStreamingRef.current = false
    }
  }, [isStreaming, isMobile])

  // Calculate available content height (viewport minus header and input)
  const getContentHeight = () => {
    // Calculate available height by subtracting the top and bottom padding from viewport height
    return viewportHeight - TOP_PADDING - BOTTOM_PADDING - ADDITIONAL_OFFSET
  }

  // Save the current selection state
  const saveSelectionState = () => {
    if (textareaRef.current) {
      selectionStateRef.current = {
        start: textareaRef.current.selectionStart,
        end: textareaRef.current.selectionEnd,
      }
    }
  }

  // Restore the saved selection state
  const restoreSelectionState = () => {
    const textarea = textareaRef.current
    const { start, end } = selectionStateRef.current

    if (textarea && start !== null && end !== null) {
      // Focus first, then set selection range
      textarea.focus()
      textarea.setSelectionRange(start, end)
    } else if (textarea) {
      // If no selection was saved, just focus
      textarea.focus()
    }
  }

  const focusTextarea = () => {
    if (textareaRef.current && !isMobile) {
      textareaRef.current.focus()
    }
  }

  const handleInputContainerClick = (e: React.MouseEvent<HTMLDivElement>) => {
    // Only focus if clicking directly on the container, not on buttons or other interactive elements
    if (
      e.target === e.currentTarget ||
      (e.currentTarget === inputContainerRef.current && !(e.target as HTMLElement).closest("button"))
    ) {
      if (textareaRef.current) {
        textareaRef.current.focus()
      }
    }
  }

  const simulateTextStreaming = async (text: string) => {
    // Split text into words
    const words = text.split(" ")
    let currentIndex = 0
    setStreamingWords([])
    setIsStreaming(true)

    return new Promise<void>((resolve) => {
      const streamInterval = setInterval(() => {
        if (currentIndex < words.length) {
          // Add a few words at a time
          const nextIndex = Math.min(currentIndex + CHUNK_SIZE, words.length)
          const newWords = words.slice(currentIndex, nextIndex)

          setStreamingWords((prev) => [
            ...prev,
            {
              id: Date.now() + currentIndex,
              text: newWords.join(" ") + " ",
            },
          ])

          currentIndex = nextIndex
        } else {
          clearInterval(streamInterval)
          resolve()
        }
      }, WORD_DELAY)
    })
  }

  const getAIResponse = async (userMessage: string) => {
    try {
      const response = await fetch(`${BASE_URL}/rag_query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userMessage
        })
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data: AIResponse = await response.json();
      console.log("Response data:", JSON.stringify(data, null, 2));
      
      // Format the message with metadata
      const formattedMessage = `${data.message}\n\n---\n
      Project Details \n-
       **Title**: ${data.metadata.title} \n-
       **Language**: ${data.metadata.language} \n-
       **Author**: ${data.metadata.created_by} \n-
       **Stars**: ${data.metadata.stars} \n-
       **Categories**: ${data.metadata.categories.join(', ')}

      Links
      **GitHub Repository**: ${data.metadata.github_link}
      **Project Website**: ${data.metadata.link}`;
      
      return formattedMessage;
    } catch (error) {
      console.error('Error fetching AI response:', error);
      return "Sorry, there was an error processing your request.";
    }
  }

  const simulateAIResponse = async (userMessage: string) => {
    const messageId = Date.now().toString()
    setStreamingMessageId(messageId)

    setMessages((prev) => [
      ...prev,
      {
        id: messageId,
        content: "",
        type: "system",
      },
    ])

    // Add vibration when streaming begins
    navigator.vibrate(50)

    try {
      const response = await getAIResponse(userMessage)
      await simulateTextStreaming(response)

      setMessages((prev) =>
        prev.map((msg) => (msg.id === messageId ? { ...msg, content: response, completed: true } : msg))
      )

      setCompletedMessages((prev) => new Set(prev).add(messageId))
    } catch (error) {
      console.error('Error in AI response:', error)
      setMessages((prev) =>
        prev.map((msg) => 
          msg.id === messageId 
            ? { ...msg, content: "Sorry, there was an error processing your request.", completed: true } 
            : msg
        )
      )
    }

    // Add vibration when streaming ends
    navigator.vibrate(50)

    setStreamingWords([])
    setStreamingMessageId(null)
    setIsStreaming(false)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value

    // Only allow input changes when not streaming
    if (!isStreaming) {
      setInputValue(newValue)

      if (newValue.trim() !== "" && !hasTyped) {
        setHasTyped(true)
      } else if (newValue.trim() === "" && hasTyped) {
        setHasTyped(false)
      }

      const textarea = textareaRef.current
      if (textarea) {
        textarea.style.height = "auto"
        const newHeight = Math.max(24, Math.min(textarea.scrollHeight, 160))
        textarea.style.height = `${newHeight}px`
      }
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputValue.trim() && !isStreaming) {
      // Add vibration when message is submitted
      navigator.vibrate(50)

      const userMessage = inputValue.trim()

      // Add as a new section if messages already exist
      const shouldAddNewSection = messages.length > 0

      const newUserMessage = {
        id: `user-${Date.now()}`,
        content: userMessage,
        type: "user" as MessageType,
        newSection: shouldAddNewSection,
      }

      // Reset input before starting the AI response
      setInputValue("")
      setHasTyped(false)
      setActiveButton("none")

      if (textareaRef.current) {
        textareaRef.current.style.height = "auto"
      }

      // Add the message after resetting input
      setMessages((prev) => [...prev, newUserMessage])

      // Only focus the textarea on desktop, not on mobile
      if (!isMobile) {
        focusTextarea()
      } else {
        // On mobile, blur the textarea to dismiss the keyboard
        if (textareaRef.current) {
          textareaRef.current.blur()
        }
      }

      // Start AI response
      simulateAIResponse(userMessage)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Handle Cmd+Enter on both mobile and desktop
    if (!isStreaming && e.key === "Enter" && e.metaKey) {
      e.preventDefault()
      handleSubmit(e)
      return
    }

    // Only handle regular Enter key (without Shift) on desktop
    if (!isStreaming && !isMobile && e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const toggleButton = (button: ActiveButton) => {
    if (!isStreaming) {
      // Save the current selection state before toggling
      saveSelectionState()

      setActiveButton((prev) => (prev === button ? "none" : button))

      // Restore the selection state after toggling
      setTimeout(() => {
        restoreSelectionState()
      }, 0)
    }
  }

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text)
      .then(() => {
        navigator.vibrate(50)
        toast("Copied to clipboard", {
          className: 'bg-primary text-secondary-foreground border-border',
          duration: 1000,
        })
      })
      .catch(err => {
        console.error('Failed to copy text: ', err)
      })
  }

  const renderMessage = (message: Message) => {
    const isCompleted = completedMessages.has(message.id)
  
    return (
      <div key={message.id} className={cn(
        "flex flex-col mb-6",
        message.type === "user" ? "items-end" : "items-start"
      )}>
        <div className={cn(
          "group relative flex max-w-4xl items-start gap-2",
          message.type === "user" ? "flex-row-reverse" : "flex-row"
        )}>
          {/* Avatar/Icon */}
          <div className={cn(
            "flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full text-sm",
            message.type === "user" 
              ? "bg-primary/10 text-primary-foreground"
              : "bg-primary/20 text-primary-foreground"
          )}>
            {message.type === "user" ? "You" : "AI"}
          </div>
  
          {/* Message Content */}
          <div className={cn(
            "flex-1 space-y-2 overflow-hidden rounded-2xl px-4 py-3",
            message.type === "user"
              ? "bg-primary/10 text-foreground"
              : "bg-secondary/50 text-secondary-foreground"
          )}>
            {message.content && (
              <div className={cn(
                "prose-sm prose-slate dark:prose-invert w-full break-words",
                message.type === "system" && !isCompleted ? "animate-fade-in" : ""
              )}>
                {message.type === 'system' ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
                  ) : (
                  message.content // Render user message as plain text
                  )}
              </div>
            )}
  
            {message.id === streamingMessageId && (
              <div className="inline prose-sm prose-slate dark:prose-invert">
                {streamingWords.map((word) => (
                  <span key={word.id} className="animate-fade-in inline">
                    {word.text}
                  </span>
                ))}
                <span className="ml-1 animate-pulse inline-block">▊</span>
              </div>
            )}
          </div>
        </div>
  
        {/* Message Actions */}
        {message.type === "system" && message.completed && (
          <div className="flex items-center gap-2 px-4 mt-2">
            <button 
              onClick={() => handleCopy(message.content)}
              className="text-xs text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1 rounded-md px-2 py-1 hover:bg-secondary/50"
            >
              <Copy className="h-3 w-3" />
              <span>Copy</span>
            </button>
          </div>
        )}
      </div>
    )
  }
  

  // Determine if a section should have fixed height (only for sections after the first)
  const shouldApplyHeight = (sectionIndex: number) => {
    return sectionIndex > 0
  }

  return (
    <div
      ref={mainContainerRef}
      className="bg-background flex flex-col overflow-hidden"
      style={{ height: isMobile ? `${viewportHeight}px` : "100svh" }}
    >
      <header className="fixed top-0 left-0 right-0 h-12 flex items-center px-4 z-20 bg-background">
        <div className="w-full flex items-center justify-between px-2">
          <a href="/">
            <h1 className="text-base font-medium text-foreground">MCP Chat</h1>
          </a>
          <div className="flex items-center space-x-1">
            <ModeToggle />
          </div>
        </div>
      </header>

      <div ref={chatContainerRef} className="flex-grow pb-32 pt-12 px-4 overflow-y-auto bg-background/50 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto space-y-2">
          {messageSections.map((section, sectionIndex) => (
            <div
              key={section.id}
              ref={sectionIndex === messageSections.length - 1 && section.isNewSection ? newSectionRef : null}
            >
              {section.isNewSection && (
                <div
                  style={
                    section.isActive && shouldApplyHeight(section.sectionIndex)
                      ? { height: `${getContentHeight()}px` }
                      : {}
                  }
                  className="pt-4 flex flex-col justify-start"
                >
                  {section.messages.map((message) => renderMessage(message))}
                </div>
              )}

              {!section.isNewSection && <div>{section.messages.map((message) => renderMessage(message))}</div>}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="fixed bottom-0 left-0 right-0 p-4 bg-background">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
          <div
            ref={inputContainerRef}
            className={cn(
              "relative w-full rounded-2xl border border-border/50 bg-background/80 backdrop-blur-sm p-3 cursor-text shadow-sm",
              isStreaming && "opacity-80",
            )}
            onClick={handleInputContainerClick}
          >
            <div className="flex items-center">
              <Textarea
              ref={textareaRef}
              placeholder={isStreaming ? "Waiting for response..." : "Ask Anything"}
              className="min-h-[24px] max-h-[160px] w-full rounded-3xl border-0 bg-transparent text-foreground dark:text-foreground placeholder:text-gray-400 placeholder:text-base focus-visible:ring-0 focus-visible:ring-offset-0 text-base pl-2 pr-4 pt-0 pb-0 resize-none overflow-y-auto leading-tight"
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              onFocus={() => {
                // Ensure the textarea is scrolled into view when focused
                if (textareaRef.current) {
                textareaRef.current.scrollIntoView({ behavior: "smooth", block: "center" })
                }
              }}
              />
              <Button
                type="submit"
                variant="outline"
                size="icon"
                className={cn(
                "rounded-full h-8 w-8 border-0 flex-shrink-0 transition-all duration-200",
                hasTyped ? "bg-primary scale-110" : "bg-secondary",
                )}
                disabled={!inputValue.trim() || isStreaming}
              >
                <ArrowUp
                className={cn(
                  "h-4 w-4 transition-colors",
                  hasTyped ? "text-primary-foreground" : "text-muted-foreground",
                )}
                />
                <span className="sr-only">Submit</span>
              </Button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}
