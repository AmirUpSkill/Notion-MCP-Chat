import { Button } from '@/components/ui/button';  
import { Switch } from '@/components/ui/switch';  
import {  Moon, FileText,  Paperclip } from 'lucide-react'; 

import type { ChatMessages } from '@/lib/types';

const messages: ChatMessages = [];

export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-4xl flex flex-col items-center gap-8">
        {/* Header: Title and Subtitle */}
        <div className="text-center space-y-2">
          <h1 className="text-5xl md:text-6xl font-bold text-foreground">
            Notion Chat
          </h1>
          <p className="text-xl text-muted-foreground max-w-md">
            AI assistant for your Notion workspace with transparent reasoning
          </p>
        </div>

        {/* Input Section Placeholder */}
        <div className="w-full max-w-2xl flex flex-col gap-4">
          <div className="relative flex items-center gap-2">
            <Button variant="ghost" size="icon" className="h-10 w-10">
              <Paperclip className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" className="h-10 w-10">
              <Moon className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" className="h-10 w-10">
              <FileText className="h-4 w-4" />
            </Button>
            {/* Notion Toggle */}
            <div className="flex items-center gap-2 px-3 py-2 rounded-md border border-border">
              <span className="text-sm text-muted-foreground">Notion</span>
              <Switch id="notion-toggle" defaultChecked />
            </div>
          </div>
          <div className="relative">
            <input
              type="text"
              placeholder="Ask about your Notion workspace..."
              className="w-full h-12 px-4 py-2 rounded-md border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>

        {/* Suggestion Pills Placeholder */}
        <div className="flex flex-wrap justify-center gap-2">
          {[
            "How do I create a new page in Notion?",
            "What's the best way to organize my workspace?",
            "Can you help me with database properties?",
            "Show me advanced Notion formulas",
            "How to use templates effectively?"
          ].map((suggestion, index) => (
            <Button
              key={index}
              variant="outline"
              size="sm"
              className="bg-secondary text-secondary-foreground rounded-full px-4 py-1"
            >
              {suggestion}
            </Button>
          ))}
        </div>
      </div>
    </main>
  );
}