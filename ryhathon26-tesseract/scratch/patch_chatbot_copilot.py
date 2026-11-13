from pathlib import Path

target = Path("EditAI/frontend/src/components/AIChatbotPanel.jsx")
text = target.read_text(encoding="utf-8")

# 1. Update component signature
old_sig = """export default function AIChatbotPanel({
  chatMessages,
  onSendCommand,
  isProcessing,
  onSelectSuggestion,
  onApplyProposal,
  onCancelProposal
}) {"""

new_sig = """export default function AIChatbotPanel({
  chatMessages,
  onSendCommand,
  isProcessing,
  onSelectSuggestion,
  onApplyProposal,
  onCancelProposal,
  onCloseCopilot
}) {"""

assert old_sig in text, "old_sig not found"
text = text.replace(old_sig, new_sig, 1)

# 2. Add Close Copilot button in the header
old_hdr_btn = """        <div className="flex items-center gap-1.5">
          <button
            onClick={() => setIsSettingsOpen(!isSettingsOpen)}
            className="flex items-center gap-1 px-1.5 py-0.5 rounded bg-[#1e2026] hover:bg-[#282a32] text-[#868a96] hover:text-[#d0d3dc] border border-[#2b2d35] transition"
            title="Configure LLM Provider (Gemini / OpenAI / Ollama / Semantic)"
          >
            <Cpu className="w-2.5 h-2.5 text-[#7ea5dc]" />
            <span className="text-[9px] font-mono">{activeBadgeLabel}</span>
            <Settings className="w-2.5 h-2.5 ml-0.5" />
          </button>
        </div>"""

new_hdr_btn = """        <div className="flex items-center gap-1">
          <button
            onClick={() => setIsSettingsOpen(!isSettingsOpen)}
            className="flex items-center gap-1 px-1.5 py-0.5 rounded bg-[#1e2026] hover:bg-[#282a32] text-[#868a96] hover:text-[#d0d3dc] border border-[#2b2d35] transition"
            title="Configure LLM Provider (Gemini / OpenAI / Ollama / Semantic)"
          >
            <Cpu className="w-2.5 h-2.5 text-[#7ea5dc]" />
            <span className="text-[9px] font-mono">{activeBadgeLabel}</span>
            <Settings className="w-2.5 h-2.5 ml-0.5" />
          </button>

          {onCloseCopilot && (
            <button
              onClick={onCloseCopilot}
              className="p-1 rounded hover:bg-[#252830] text-[#7a808e] hover:text-white transition ml-0.5 cursor-pointer"
              title="Close Copilot Panel (Click AI Assistant to re-open anytime)"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>"""

assert old_hdr_btn in text, "old_hdr_btn not found"
text = text.replace(old_hdr_btn, new_hdr_btn, 1)

target.write_text(text, encoding="utf-8")
print("AIChatbotPanel.jsx patched with onCloseCopilot successfully!")

