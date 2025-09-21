export enum SSEEventType {
  AGENT_START = 'agent_start',
  REASONING = 'reasoning',
  TOOL_CALL = 'tool_call',
  FINAL_ANSWER = 'final_answer',
  STREAM_END = 'stream_end',
}

export type MessageRole = 'user' | 'assistant';

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  createdAt?: Date;
  metadata?: {
    sources?: string[];
  };
}

export interface AgentStartPayload {
  status: 'started';
}

export interface ReasoningPayload {
  reasoning: string;
}

export interface ToolCallPayload {
  tool: string;
  args: Record<string, any>;
  result?: string;
}

export interface FinalAnswerPayload {
  answer: string;
}

export interface StreamEndPayload {
  status: 'finished';
}

export interface SSEEvent {
  type: SSEEventType;
  data: 
    | AgentStartPayload
    | ReasoningPayload
    | ToolCallPayload
    | FinalAnswerPayload
    | StreamEndPayload;
}

export interface AgentStep {
  id: string;
  type: SSEEventType.REASONING | SSEEventType.TOOL_CALL;
  payload: ReasoningPayload | ToolCallPayload;
  timestamp: Date;
}

export type ChatMessages = ChatMessage[];
export type AgentSteps = AgentStep[];

export interface ChatRequest {
  message: string;
  enable_notion?: boolean;
}