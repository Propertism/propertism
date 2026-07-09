document.addEventListener('DOMContentLoaded', function() {
    const rootEl = document.getElementById('admin-chat-viewer-root');
    if (!rootEl) return;

    let transcriptData = [];
    try {
        transcriptData = JSON.parse(rootEl.getAttribute('data-transcript') || '[]');
    } catch (e) {
        console.error("Error parsing transcript data", e);
    }

    if (!Array.isArray(transcriptData)) {
        transcriptData = [];
    }

    function ChatViewer() {
        if (transcriptData.length === 0) {
            return React.createElement('div', {
                style: {
                    padding: '20px',
                    color: '#64748b',
                    textAlign: 'center',
                    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                    fontSize: '13px'
                }
            }, 'No chat history recorded for this session.');
        }

        return React.createElement('div', {
            style: {
                fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                padding: '16px',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
                background: '#f8fafc',
                border: '1px solid #e2e8f0',
                borderRadius: '4px',
                maxHeight: '600px',
                overflowY: 'auto',
                boxShadow: 'inset 0 2px 4px 0 rgba(0,0,0,0.02)'
            }
        }, transcriptData.map((msg, idx) => {
            const isUser = msg.sender === 'user' || msg.type === 'user';
            const isAdvisor = msg.type === 'advisor';
            
            const align = isUser ? 'flex-end' : 'flex-start';
            const bg = isUser ? '#f1f5f9' : (isAdvisor ? '#fefcbf' : '#ffffff');
            const border = isUser ? '1px solid #cbd5e1' : (isAdvisor ? '1px solid #fef08a' : '1px solid #e2e8f0');
            const leftBorder = isUser ? '1px solid #cbd5e1' : (isAdvisor ? '4px solid #d97706' : '4px solid #c8a24a');
            
            let label = 'realBOT ADVISOR';
            if (isUser) {
                label = 'CLIENT CONSULTANT';
            } else if (isAdvisor) {
                label = `HUMAN ADVISOR (${msg.sender || 'Advisor'})`;
            }

            let formattedTime = '';
            if (msg.created_at) {
                try {
                    const date = new Date(msg.created_at);
                    formattedTime = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' ' + date.toLocaleDateString();
                } catch(e) {
                    formattedTime = msg.created_at;
                }
            }

            return React.createElement('div', {
                key: idx,
                style: {
                    alignSelf: align,
                    maxWidth: '85%',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '4px'
                }
            }, [
                React.createElement('div', {
                    style: {
                        fontSize: '9px',
                        fontWeight: 'bold',
                        color: '#94a3b8',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em',
                        alignSelf: isUser ? 'flex-end' : 'flex-start',
                        padding: '0 4px'
                    }
                }, `${label} - ${formattedTime}`),
                React.createElement('div', {
                    style: {
                        background: bg,
                        border: border,
                        borderLeft: leftBorder,
                        padding: '10px 14px',
                        borderRadius: '2px',
                        fontSize: '13px',
                        lineHeight: '1.5',
                        color: '#1e293b',
                        whiteSpace: 'pre-wrap',
                        boxShadow: '0 1px 2px 0 rgba(0,0,0,0.05)'
                    }
                }, msg.text || msg.message_text || '')
            ]);
        }));
    }

    const root = ReactDOM.createRoot(rootEl);
    root.render(React.createElement(ChatViewer));
});
