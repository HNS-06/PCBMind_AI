import { create } from 'zustand';
import type { Project, ChatMessage } from '@/types';

interface AppState {
  currentProject: Project | null;
  projects: Project[];
  chatMessages: ChatMessage[];
  conversationId: string | null;
  isGenerating: boolean;
  setCurrentProject: (project: Project | null) => void;
  setProjects: (projects: Project[]) => void;
  addChatMessage: (message: ChatMessage) => void;
  setConversationId: (id: string | null) => void;
  setIsGenerating: (val: boolean) => void;
  clearChat: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  currentProject: null,
  projects: [],
  chatMessages: [],
  conversationId: null,
  isGenerating: false,
  setCurrentProject: (project) => set({ currentProject: project }),
  setProjects: (projects) => set({ projects }),
  addChatMessage: (message) => set((state) => ({
    chatMessages: [...state.chatMessages, message],
  })),
  setConversationId: (id) => set({ conversationId: id }),
  setIsGenerating: (val) => set({ isGenerating: val }),
  clearChat: () => set({ chatMessages: [], conversationId: null }),
}));
