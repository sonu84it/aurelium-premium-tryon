import { create } from "zustand";

import type { AnalyzeResponse, GenerateResponse, JewelleryType, StoneType, UploadResponse, MetalType } from "@/types";

interface AureliumState {
  upload?: UploadResponse;
  analysis?: AnalyzeResponse;
  results?: GenerateResponse;
  selectedCategory: JewelleryType;
  selectedMetal: MetalType;
  selectedStone: StoneType;
  setUpload: (upload: UploadResponse) => void;
  setAnalysis: (analysis: AnalyzeResponse) => void;
  setResults: (results: GenerateResponse) => void;
  setSelectedCategory: (category: JewelleryType) => void;
  setSelectedMetal: (metal: MetalType) => void;
  setSelectedStone: (stone: StoneType) => void;
}

export const useAurelium = create<AureliumState>((set) => ({
  selectedCategory: "earrings",
  selectedMetal: "yellow_gold",
  selectedStone: "diamond",
  setUpload: (upload) => set({ upload }),
  setAnalysis: (analysis) => set({ analysis }),
  setResults: (results) => set({ results }),
  setSelectedCategory: (selectedCategory) => set({ selectedCategory }),
  setSelectedMetal: (selectedMetal) => set({ selectedMetal }),
  setSelectedStone: (selectedStone) => set({ selectedStone }),
}));
