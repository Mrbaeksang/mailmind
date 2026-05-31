export type Category = "urgent" | "action" | "newsletter" | "spam";

export interface Email {
  _id: string;
  threadId: string;
  from: string;
  to: string[];
  subject: string;
  body: string;
  date: string | null;
  category: Category | null;
}

export interface ThreadInsight {
  _id: string;
  summary: string[];
  todos: string[];
  draftId: string | null;
}

export interface SearchHit {
  _id: string;
  subject: string;
  from?: string;
  category?: Category;
  score?: number;
}
