import React, { useState, useRef, useEffect } from 'react';
import PropertyCard from './PropertyCard';

/**
 * RealBot - Polished AI assistant sliding panel component.
 * Behave similarly to Microsoft Copilot or ChatGPT Sidebar.
 * Preserves luxury real estate corporate branding: flat design, sharp rectangular shapes,
 * navy/gold colors, zero rounded cards or buttons, minimal visual noise.
 */
export default function RealBot({ isOpen = true, onClose = () => {} }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      time: '12:00 PM',
      type: 'text',
      text: `Welcome to **realBOT**, the premium advisory portal for **Propertism**.
As your digital private wealth manager, I provide institutional-grade advisory on luxury real estate assets in Chennai and key markets.

How may I assist you with your property portfolio today?`,
      chips: ['Luxury Villas', 'Apartments', 'Plots', 'NRI Investment', 'Rental Homes', 'Compare Projects']
    }
  ]);

  const [inputVal, setInputVal] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSend = (textToSend) => {
    const text = textToSend || inputVal;
    if (!text.trim()) return;

    // Add user message
    const userMsg = {
      id: Date.now(),
      sender: 'user',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      type: 'text',
      text: text
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputVal('');
    setIsTyping(true);

    // Simulate realBOT advisor response
    setTimeout(() => {
      let responseDetails = {
        text: `I have received your request: "${text}". An investment advisor will prepare a report for you.`,
        chips: ['Luxury Villas', 'Apartments', 'NRI Investment']
      };

      const query = text.toLowerCase();
      if (query.includes('villa') || query.includes('luxury') || query.includes('villas')) {
        responseDetails = {
          text: 'I have retrieved our prime listing in the luxury villa segment located in Chennai ECR:',
          property: {
            imageUrl: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80',
            badge: 'PREMIUM ASSET',
            name: 'The Oceanfront Manor',
            location: 'VGP Layout, ECR, Chennai',
            price: '₹4.90 Crore',
            configuration: '4 BHK Beach Villa',
            area: '4,500 Sq.Ft.',
            builder: 'Oceanic Developers',
            highlights: ['Beachfront Access', 'Private Gardens', 'High Security']
          },
          chips: ['View Details', 'Compare Properties', 'Schedule Visit', 'Show Similar']
        };
      } else if (query.includes('nri') || query.includes('investment') || query.includes('investments')) {
        responseDetails = {
          text: 'For NRI investors, commercial real estate allocations in Chennai deliver high yield stability [1].',
          comparison: {
            title: 'NRI Investment Performance Matrix',
            headers: ['Asset Type', 'Growth (YoY)', 'Rental Yield', 'Regulatory Ease'],
            rows: [
              ['Commercial Office', '8.5%', '7.2% - 8.5%', 'High (Pre-leased)'],
              ['Premium ECR Villas', '12.0%', '3.5% - 4.2%', 'Medium (RERA Ready)'],
              ['OMR Apartments', '6.0%', '4.5% - 5.0%', 'High (Ready to Move)']
            ]
          },
          citations: [
            '[1] RBI Repatriation Circular 2026.',
            '[2] Propertism Q2 Index.',
            '[3] Chennai Residential Bulletin 2026.'
          ],
          chips: ['Filter by Budget', 'Ready to Move', 'Under ₹75 Lakhs']
        };
      } else if (query.includes('apartment') || query.includes('budget') || query.includes('apartments') || query.includes('plots')) {
        responseDetails = {
          text: 'Here is our curated apartment listing matching your budget criteria:',
          property: {
            imageUrl: 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80',
            badge: 'VALUE PORTFOLIO',
            name: 'Meridian Heights Complex',
            location: 'Medavakkam, Chennai',
            price: '₹72 Lakhs',
            configuration: '2.5 BHK Apartment',
            area: '1,280 Sq.Ft.',
            builder: 'Meridian Builders',
            highlights: ['Near Metro Station', 'Reserved Parking', 'Under Construction']
          },
          chips: ['Luxury Villas', 'Compare Projects', 'Ready to Move']
        };
      }

      const assistantMsg = {
        id: Date.now() + 1,
        sender: 'assistant',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        type: 'rich',
        ...responseDetails
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setIsTyping(false);
    }, 1100);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9900] flex justify-end">
      {/* Backdrop overlay (15-20% transparent overlay) */}
      <div 
        onClick={onClose}
        className="absolute inset-0 bg-[#0f172a]/18 transition-opacity duration-300"
      ></div>

      {/* Right-Side Sliding Panel (Desktop: 520px-560px width, Mobile: 100%) */}
      <div className="relative w-full sm:w-[540px] h-full bg-white flex flex-col justify-between shadow-2xl z-10 transition-transform duration-300 ease-out select-none border-l border-[#0E2A47]/10 overflow-hidden rounded-none">
        
        {/* Panel Header: transparent background, Close X icon only, no borders or background */}
        <div className="h-12 bg-transparent px-4 flex items-center justify-end shrink-0 select-none z-10">
          <button onClick={onClose} className="text-[#0E2A47] hover:text-[#C89B2B] p-1 bg-transparent border-0 outline-none shadow-none focus:outline-none" title="Close Panel">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>

        {/* Conversation Viewport */}
        <div className="flex-1 overflow-y-auto bg-[#F7F8FA] p-6 flex flex-col gap-6">
          {messages.map((msg) => (
            <div key={msg.id} className="w-full flex flex-col">
              <div className="flex justify-between items-center text-[9px] text-gray-400 font-semibold tracking-wider uppercase mb-1.5 px-1">
                <span>{msg.sender === 'user' ? 'CLIENT CONSULTANT' : 'realBOT ADVISOR'}</span>
                <span>{msg.time}</span>
              </div>
              <div className="w-full p-5 border border-[#0E2A47]/10 bg-white text-xs leading-relaxed text-gray-800 space-y-3">
                {msg.text.split('\n\n').map((paragraph, idx) => {
                  if (paragraph.startsWith('### ')) {
                    return <h4 key={idx} className="text-xs font-bold text-[#0E2A47] uppercase tracking-wider mt-3 border-b border-[#0E2A47]/5 pb-1">{paragraph.replace('### ', '')}</h4>;
                  }
                  const parts = paragraph.split('**');
                  return (
                    <p key={idx}>
                      {parts.map((p, pIdx) => pIdx % 2 === 1 ? <strong key={pIdx} className="font-bold text-[#0E2A47]">{p}</strong> : p)}
                    </p>
                  );
                })}

                {/* Property Recommendation Card (Informational Only) */}
                {msg.property && (
                  <PropertyCard
                    imageUrl={msg.property.imageUrl}
                    badge={msg.property.badge}
                    name={msg.property.name}
                    location={msg.property.location}
                    price={msg.property.price}
                    configuration={msg.property.configuration}
                    area={msg.property.area}
                    builder={msg.property.builder}
                    highlights={msg.property.highlights}
                  />
                )}

                {/* Tabular comparisons */}
                {msg.comparison && (
                  <div className="border border-[#0E2A47]/10 mt-3 overflow-x-auto">
                    <table className="w-full text-left text-[11px]">
                      <thead>
                        <tr className="bg-[#F7F8FA] border-b border-[#0E2A47]/10 font-bold text-[#0E2A47]">
                          {msg.comparison.headers.map((h, idx) => <th key={idx} className="p-2 uppercase tracking-wider text-[8px]">{h}</th>)}
                        </tr>
                      </thead>
                      <tbody>
                        {msg.comparison.rows.map((row, rIdx) => (
                          <tr key={rIdx} className="border-b border-[#0E2A47]/5 last:border-b-0 bg-white">
                            {row.map((cell, cIdx) => <td key={cIdx} className="p-2 text-gray-600 font-medium">{cell}</td>)}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}

                {/* Citations block */}
                {msg.citations && (
                  <div className="pt-2 border-t border-[#0E2A47]/5 text-[9px] text-gray-400 italic flex flex-col gap-0.5">
                    {msg.citations.map((cite, idx) => <span key={idx}>{cite}</span>)}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="w-full flex flex-col">
              <div className="text-[9px] text-gray-400 font-semibold tracking-wider uppercase mb-1.5 px-1">realBOT ADVISOR</div>
              <div className="bg-white border border-[#0E2A47]/10 p-4 flex items-center gap-3">
                <div className="flex gap-1.5">
                  <span className="w-1.5 h-1.5 bg-[#0E2A47] animate-pulse"></span>
                  <span className="w-1.5 h-1.5 bg-[#C89B2B] animate-pulse [animation-delay:150ms]"></span>
                  <span className="w-1.5 h-1.5 bg-[#0E2A47] animate-pulse [animation-delay:300ms]"></span>
                </div>
                <span className="text-[10px] font-bold text-[#0E2A47] uppercase tracking-wider">
                  realBOT is checking market indices...
                </span>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Dynamic Suggestion Chips Container */}
        {messages.length > 0 && messages[messages.length - 1].chips && (
          <div className="px-6 py-3 bg-white border-t border-[#0E2A47]/10 shrink-0">
            <div className="flex gap-2 overflow-x-auto py-1 no-scrollbar">
              {messages[messages.length - 1].chips.map((chip, idx) => (
                <button 
                  key={idx}
                  onClick={() => handleSend(chip)}
                  className="px-3 py-1.5 border border-[#0E2A47] text-[#0E2A47] hover:bg-[#C89B2B] hover:border-[#C89B2B] hover:text-white transition-all duration-150 text-[9px] font-bold uppercase tracking-wider whitespace-nowrap rounded-none bg-white"
                >
                  {chip}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area (Textarea + icons, permanently bottom pinned) */}
        <div className="p-4 bg-white border-t border-[#0E2A47]/10 shrink-0">
          <div className="flex border border-[#0E2A47] rounded-none bg-[#F7F8FA] overflow-hidden items-stretch px-3">
            <button className="text-gray-400 hover:text-[#0E2A47] px-1.5 transition-colors self-end pb-3 bg-transparent border-0 outline-none shadow-none focus:outline-none" title="Attach">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
            </button>
            <textarea 
              value={inputVal}
              onChange={(e) => setInputVal(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask realBOT anything about properties..."
              rows={1}
              className="flex-1 bg-transparent border-0 outline-none text-xs px-2 py-3 text-[#0E2A47] placeholder-gray-400 font-sans resize-none min-h-[36px] max-h-[120px] leading-relaxed"
            />

            {/* Vertical Divider */}
            <div className="w-px bg-[#0E2A47]/10 self-stretch my-2.5 mx-1.5 shrink-0"></div>

            <button 
              onClick={() => handleSend()}
              className="text-[#0E2A47] hover:text-[#C89B2B] px-1.5 transition-colors self-end pb-3 bg-transparent border-0 outline-none shadow-none focus:outline-none"
              title="Send"
            >
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
