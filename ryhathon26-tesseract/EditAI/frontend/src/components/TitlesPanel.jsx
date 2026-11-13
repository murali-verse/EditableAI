import React, { useState } from 'react';
import {
  Type,
  Sparkles,
  CheckCircle2,
  Plus,
  Palette,
  Clock,
  Sliders,
  AlignLeft,
  AlignCenter
} from 'lucide-react';
import { formatTimecode } from '../utils/timeUtils';

const TITLE_TEMPLATES = [
  {
    id: 'lower_third',
    name: 'Broadcast Lower Third',
    category: 'Speaker ID',
    defaultMain: 'Keynote Speaker: Dr. Elena Vance',
    defaultSub: 'Director of AI Systems & Vision',
    color: '#38bdf8',
    position: 'bottom-left'
  },
  {
    id: 'cinematic_headline',
    name: 'Cinematic Title',
    category: 'Title',
    defaultMain: 'PROJECT HORIZON',
    defaultSub: 'A New Era in Visual Intelligence',
    color: '#fbbf24',
    position: 'center'
  },
  {
    id: 'bold_social',
    name: 'Bold Social Callout',
    category: 'Highlight',
    defaultMain: 'REVOLUTIONARY SPEED',
    defaultSub: 'Over 10x faster rendering workflows',
    color: '#f43f5e',
    position: 'center'
  },
  {
    id: 'subtitle_banner',
    name: 'Minimal Subtitle Banner',
    category: 'Captions',
    defaultMain: 'Synchronized visual sequence beat',
    defaultSub: '',
    color: '#ffffff',
    position: 'bottom'
  },
  {
    id: 'neon_cyber',
    name: 'Neon Cyber Callout',
    category: 'Stylized',
    defaultMain: 'NEXT-GEN EDITING',
    defaultSub: 'AI Story Architecture',
    color: '#c084fc',
    position: 'top-left'
  }
];

export default function TitlesPanel({
  currentTime = 0,
  onInsertTitle
}) {
  const [selectedTemplateId, setSelectedTemplateId] = useState('lower_third');
  const [mainText, setMainText] = useState('Keynote Speaker: Dr. Elena Vance');
  const [subText, setSubText] = useState('Director of AI Systems & Vision');
  const [textColor, setTextColor] = useState('#38bdf8');
  const [duration, setDuration] = useState(3.5);
  const [appliedNotice, setAppliedNotice] = useState(null);

  const selectedTemplate = TITLE_TEMPLATES.find((t) => t.id === selectedTemplateId) || TITLE_TEMPLATES[0];

  const handleSelectTemplate = (template) => {
    setSelectedTemplateId(template.id);
    setMainText(template.defaultMain);
    setSubText(template.defaultSub);
    setTextColor(template.color);
  };

  const handleInsert = () => {
    if (!mainText.trim()) return;

    const fullText = subText.trim() ? `${mainText.trim()} — ${subText.trim()}` : mainText.trim();

    if (onInsertTitle) {
      onInsertTitle({
        templateId: selectedTemplateId,
        title: mainText.trim(),
        subtitle: subText.trim(),
        fullText,
        color: textColor,
        duration,
        startTime: currentTime,
        endTime: currentTime + duration
      });
    }

    setAppliedNotice(`Inserted title "${mainText.slice(0, 18)}..." at ${formatTimecode(currentTime)}`);
    setTimeout(() => setAppliedNotice(null), 3000);
  };

  return (
    <div className="h-full flex flex-col bg-[#141518] text-[#a0a4ae] select-none text-[11px] overflow-hidden">
      {/* 1. Header */}
      <div className="h-8 px-3 border-b border-[#212328] flex items-center justify-between bg-[#18191d]">
        <div className="flex items-center gap-1.5 text-[#d0d3dc] font-medium">
          <Type className="w-3.5 h-3.5 text-[#c084fc]" />
          <span>Titles & Text Generator</span>
        </div>
        <span className="text-[10px] text-[#787d8c] font-mono">
          Playhead: {formatTimecode(currentTime)}
        </span>
      </div>

      {/* 2. Interactive Title Customization */}
      <div className="p-2.5 border-b border-[#212328] bg-[#121316] space-y-2">
        {/* Main Text */}
        <div className="space-y-1">
          <label className="text-[10px] text-[#7a808e] font-medium block uppercase tracking-wider">
            Header / Speaker Name
          </label>
          <input
            type="text"
            value={mainText}
            onChange={(e) => setMainText(e.target.value)}
            placeholder="Title heading..."
            className="w-full bg-[#17181c] border border-[#24262c] rounded px-2 py-1 text-[#e1e4ed] text-[11px] focus:outline-none focus:border-[#7c3aed]"
          />
        </div>

        {/* Sub Text */}
        <div className="space-y-1">
          <label className="text-[10px] text-[#7a808e] font-medium block uppercase tracking-wider">
            Tagline / Sub-Text (Optional)
          </label>
          <input
            type="text"
            value={subText}
            onChange={(e) => setSubText(e.target.value)}
            placeholder="Subtitle description..."
            className="w-full bg-[#17181c] border border-[#24262c] rounded px-2 py-1 text-[#b5b9c4] text-[10px] focus:outline-none focus:border-[#7c3aed]"
          />
        </div>

        {/* Color Palette & Duration */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-1.5">
            <span className="text-[10px] text-[#7a808e]">Accent:</span>
            {['#38bdf8', '#fbbf24', '#f43f5e', '#ffffff', '#c084fc', '#34d399'].map((c) => (
              <button
                key={c}
                onClick={() => setTextColor(c)}
                style={{ backgroundColor: c }}
                className={`w-3.5 h-3.5 rounded-full transition ${textColor === c ? 'ring-2 ring-white scale-110' : 'opacity-80 hover:opacity-100'}`}
              />
            ))}
          </div>

          <div className="flex items-center gap-1 font-mono text-[10px] text-[#a0a4ae]">
            <Clock className="w-3 h-3 text-[#7a808e]" />
            <span>{duration.toFixed(1)}s</span>
          </div>
        </div>

        {appliedNotice && (
          <div className="flex items-center gap-1.5 text-[10px] text-[#5bb676] bg-[#17241b] border border-[#223d2a] px-2 py-1 rounded">
            <CheckCircle2 className="w-3 h-3 shrink-0" />
            <span className="truncate">{appliedNotice}</span>
          </div>
        )}
      </div>

      {/* 3. Title Templates List */}
      <div className="flex-1 overflow-y-auto p-2.5 space-y-2">
        <span className="text-[10px] font-medium text-[#7a808e] block uppercase tracking-wider">
          Style Presets
        </span>
        <div className="space-y-1.5">
          {TITLE_TEMPLATES.map((tmpl) => {
            const isSelected = selectedTemplateId === tmpl.id;
            return (
              <div
                key={tmpl.id}
                onClick={() => handleSelectTemplate(tmpl)}
                className={`p-2 rounded border cursor-pointer transition ${
                  isSelected
                    ? 'bg-[#261c30] border-[#7c3aed] shadow-xs text-[#c084fc]'
                    : 'bg-[#17181c] hover:bg-[#1d1f25] border-[#22242a]'
                }`}
              >
                <div className="flex items-center justify-between text-[11px] mb-1">
                  <span className="font-medium text-[#d8dbe4]">{tmpl.name}</span>
                  <span className="text-[9px] font-mono px-1 py-0.2 rounded bg-[#101114] text-[#808696] border border-[#212328]">
                    {tmpl.category}
                  </span>
                </div>

                {/* Mini Visual Preview */}
                <div className="bg-[#0f1013] border border-[#212328] rounded p-1.5 flex flex-col justify-center">
                  <span style={{ color: tmpl.color }} className="font-bold text-[10px] tracking-wide truncate">
                    {tmpl.defaultMain}
                  </span>
                  {tmpl.defaultSub && (
                    <span className="text-[8px] text-[#888e9d] truncate">
                      {tmpl.defaultSub}
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 4. Footer Insert Action */}
      <div className="p-2 border-t border-[#212328] bg-[#16171b] flex items-center justify-between">
        <span className="text-[10px] text-[#6f7482]">
          Starts: <span className="font-mono text-[#a0a4ae]">{formatTimecode(currentTime)}</span>
        </span>
        <button
          onClick={handleInsert}
          disabled={!mainText.trim()}
          className="px-3 py-1 rounded bg-[#261c30] hover:bg-[#351e4c] border border-[#7c3aed] text-[#c084fc] text-[10px] font-medium flex items-center gap-1.5 transition shadow-xs disabled:opacity-40"
        >
          <Plus className="w-3 h-3 text-[#c084fc]" />
          <span>Insert at Playhead</span>
        </button>
      </div>
    </div>
  );
}

