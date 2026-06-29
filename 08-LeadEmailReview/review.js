// 08-LeadEmailReview/review.js

const scenarios = [
    {
        id: 'genuine-owner',
        name: 'Genuine Property Owner',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8942',
            priority: 'High Priority',
            score: '97%',
            scoreColor: 'success',
            status: 'Likely Genuine',
            validations: [
                { text: 'Valid Phone Format', type: 'success' },
                { text: 'Human Name Format', type: 'success' },
                { text: 'Relevant Property Intent', type: 'success' },
                { text: 'No Suspicious URLs', type: 'success' },
                { text: 'No Spam Keywords', type: 'success' }
            ],
            customerName: 'Karthik Subbaraj',
            phone: '+91 98401 23456',
            email: 'karthik.s@example.com',
            city: 'Chennai, India',
            source: 'Property Detail Form',
            intent: 'Sell Property',
            message: 'I own a 3BHK in Adyar and am looking to sell it within the next 3 months. Please contact me to discuss valuation and process.',
            received: 'Oct 14, 2026 at 09:30 AM'
        }
    },
    {
        id: 'nri-owner',
        name: 'Genuine NRI Owner',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8943',
            priority: 'High Priority',
            score: '94%',
            scoreColor: 'success',
            status: 'Likely Genuine',
            validations: [
                { text: 'Valid Intl Phone', type: 'success' },
                { text: 'Human Name Format', type: 'success' },
                { text: 'Relevant Property Intent', type: 'success' },
                { text: 'No Suspicious URLs', type: 'success' },
                { text: 'No Spam Keywords', type: 'success' }
            ],
            customerName: 'Anita Krishnan',
            phone: '+1 415 555 0198',
            email: 'anita.k@example.com',
            city: 'San Francisco, USA',
            source: 'General Inquiry',
            intent: 'Property Management',
            message: 'I have two apartments in OMR. I need end-to-end property management services since I live in the US.',
            received: 'Oct 14, 2026 at 11:15 PM'
        }
    },
    {
        id: 'management-inquiry',
        name: 'Property Management Inquiry',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8944',
            priority: 'Standard Priority',
            score: '88%',
            scoreColor: 'success',
            status: 'Likely Genuine',
            validations: [
                { text: 'Valid Phone Format', type: 'success' },
                { text: 'Human Name Format', type: 'success' },
                { text: 'Relevant Property Intent', type: 'success' },
                { text: 'No Suspicious URLs', type: 'success' },
                { text: 'No Spam Keywords', type: 'success' }
            ],
            customerName: 'Suresh Kumar',
            phone: '+91 99400 11223',
            email: 'suresh@example.in',
            city: 'Bangalore, India',
            source: 'Services Page Form',
            intent: 'Property Management',
            message: 'Looking for a reliable agency to manage my villa in ECR. What are your charges?',
            received: 'Oct 15, 2026 at 10:05 AM'
        }
    },
    {
        id: 'callback-request',
        name: 'Callback Request',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8945',
            priority: 'High Priority',
            score: '82%',
            scoreColor: 'success',
            status: 'Likely Genuine',
            validations: [
                { text: 'Valid Phone Format', type: 'success' },
                { text: 'Human Name Format', type: 'success' },
                { text: 'Short Message', type: 'warning' },
                { text: 'No Suspicious URLs', type: 'success' },
                { text: 'No Spam Keywords', type: 'success' }
            ],
            customerName: 'Priya Rajan',
            phone: '+91 98844 55667',
            email: 'priya.r@example.com',
            city: 'Chennai, India',
            source: 'Quick Inquiry',
            intent: 'Buy Property',
            message: 'Please call me back.',
            received: 'Oct 15, 2026 at 02:20 PM'
        }
    },
    {
        id: 'potential-spam',
        name: 'Potential Spam',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8946',
            priority: 'Low Priority',
            score: '54%',
            scoreColor: 'warning',
            status: 'Review Recommended',
            validations: [
                { text: 'Invalid Phone Format', type: 'danger' },
                { text: 'Unusual Name', type: 'warning' },
                { text: 'Vague Intent', type: 'warning' },
                { text: 'No Suspicious URLs', type: 'success' },
                { text: 'Promotional Language', type: 'warning' }
            ],
            customerName: 'Best SEO Services',
            phone: '0000000000',
            email: 'sales@bestseo.example',
            city: 'Unknown',
            source: 'General Inquiry',
            intent: 'Other',
            message: 'Do you want to rank higher on Google? We offer the best SEO services for real estate websites. Reply to this email for a free audit.',
            received: 'Oct 15, 2026 at 04:45 PM'
        }
    },
    {
        id: 'foreign-spam',
        name: 'Foreign Language Spam',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8947',
            priority: 'Low Priority',
            score: '32%',
            scoreColor: 'danger',
            status: 'Likely Spam',
            validations: [
                { text: 'Invalid Phone Format', type: 'danger' },
                { text: 'Foreign Language Detected', type: 'danger' },
                { text: 'No Property Intent', type: 'danger' },
                { text: 'No Suspicious URLs', type: 'success' },
                { text: 'No Spam Keywords', type: 'success' }
            ],
            customerName: 'Ivanov',
            phone: '+7 999 123 4567',
            email: 'ivanov@example.ru',
            city: 'Unknown',
            source: 'General Inquiry',
            intent: 'Other',
            message: 'Здравствуйте, предлагаем услуги по продвижению.',
            received: 'Oct 15, 2026 at 08:12 PM'
        }
    },
    {
        id: 'url-spam',
        name: 'URL Spam',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8948',
            priority: 'Low Priority',
            score: '12%',
            scoreColor: 'danger',
            status: 'High Risk Spam',
            validations: [
                { text: 'Invalid Phone Format', type: 'danger' },
                { text: 'Bot-like Name', type: 'danger' },
                { text: 'External URL Detected', type: 'danger' },
                { text: 'Multiple Hyperlinks', type: 'danger' },
                { text: 'Spam Keywords Found', type: 'danger' }
            ],
            customerName: 'Crypto Investment',
            phone: '1231231234',
            email: 'invest@crypto.example',
            city: 'Unknown',
            source: 'Quick Inquiry',
            intent: 'Other',
            message: 'Earn 500% ROI in 2 weeks! Click here: https://crypto.example/scam and here http://bit.ly/scam2 to get rich quick.',
            received: 'Oct 16, 2026 at 01:05 AM'
        }
    },
    {
        id: 'empty-message',
        name: 'Empty Message',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8949',
            priority: 'Standard Priority',
            score: '75%',
            scoreColor: 'warning',
            status: 'Review Recommended',
            validations: [
                { text: 'Valid Phone Format', type: 'success' },
                { text: 'Human Name Format', type: 'success' },
                { text: 'Message Body Empty', type: 'warning' },
                { text: 'No Suspicious URLs', type: 'success' },
                { text: 'No Spam Keywords', type: 'success' }
            ],
            customerName: 'Ramesh Babu',
            phone: '+91 94444 55555',
            email: 'ramesh.b@example.com',
            city: 'Chennai, India',
            source: 'Quick Inquiry',
            intent: 'Rent Out Property',
            message: '',
            received: 'Oct 16, 2026 at 11:30 AM'
        }
    },
    {
        id: 'missing-phone',
        name: 'Missing Phone',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8950',
            priority: 'Standard Priority',
            score: '72%',
            scoreColor: 'warning',
            status: 'Review Recommended',
            validations: [
                { text: 'Phone Not Provided', type: 'warning' },
                { text: 'Human Name Format', type: 'success' },
                { text: 'Relevant Property Intent', type: 'success' },
                { text: 'No Suspicious URLs', type: 'success' },
                { text: 'No Spam Keywords', type: 'success' }
            ],
            customerName: 'Deepa V',
            phone: 'Not Provided',
            email: 'deepa.v@example.com',
            city: 'Unknown',
            source: 'General Inquiry',
            intent: 'Buy Property',
            message: 'Can you share the brochure for the OMR project?',
            received: 'Oct 16, 2026 at 03:45 PM'
        }
    },
    {
        id: 'missing-email',
        name: 'Missing Email',
        data: {
            title: 'Property Lead Notification',
            ref: 'LEAD-2026-8951',
            priority: 'High Priority',
            score: '85%',
            scoreColor: 'success',
            status: 'Likely Genuine',
            validations: [
                { text: 'Valid Phone Format', type: 'success' },
                { text: 'Email Not Provided', type: 'warning' },
                { text: 'Human Name Format', type: 'success' },
                { text: 'No Suspicious URLs', type: 'success' },
                { text: 'No Spam Keywords', type: 'success' }
            ],
            customerName: 'Murali K',
            phone: '+91 98400 98400',
            email: 'Not Provided',
            city: 'Chennai, India',
            source: 'Quick Inquiry',
            intent: 'Sell Property',
            message: 'Need to sell my plot in ECR. Call me.',
            received: 'Oct 17, 2026 at 10:10 AM'
        }
    }
];

function initReviewApp() {
    const listEl = document.getElementById('scenario-list');
    
    // Render scenario buttons
    scenarios.forEach((scenario, index) => {
        const btn = document.createElement('button');
        btn.className = 'scenario-btn' + (index === 0 ? ' active' : '');
        btn.textContent = scenario.name;
        btn.onclick = () => {
            document.querySelectorAll('.scenario-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderScenario(scenario.data);
        };
        listEl.appendChild(btn);
    });
    
    // Viewport controls
    document.querySelectorAll('.viewport-btn').forEach(btn => {
        btn.onclick = (e) => {
            document.querySelectorAll('.viewport-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const container = document.getElementById('preview-container');
            container.className = 'preview-container ' + btn.dataset.view;
        };
    });

    // Initial render
    renderScenario(scenarios[0].data);
}

function renderScenario(data) {
    document.getElementById('exec-ref').textContent = data.ref;
    document.getElementById('exec-priority').textContent = data.priority;
    
    const scoreEl = document.getElementById('score-value');
    scoreEl.textContent = data.score;
    scoreEl.className = 'score-value ' + (data.scoreColor !== 'success' ? data.scoreColor : '');
    
    document.getElementById('assessment-status').textContent = data.status;
    
    const valGrid = document.getElementById('validation-grid');
    valGrid.innerHTML = '';
    data.validations.forEach(val => {
        const item = document.createElement('div');
        item.className = 'val-item ' + val.type;
        
        let icon = '';
        if (val.type === 'success') icon = '✓';
        if (val.type === 'warning') icon = '⚠';
        if (val.type === 'danger') icon = '⚠';
        
        item.innerHTML = `<span>${icon}</span> <span>${val.text}</span>`;
        valGrid.appendChild(item);
    });
    
    document.getElementById('val-name').textContent = data.customerName;
    document.getElementById('val-phone').textContent = data.phone;
    document.getElementById('val-email').textContent = data.email;
    document.getElementById('val-city').textContent = data.city;
    
    document.getElementById('req-badge').textContent = data.intent;
    
    const msgEl = document.getElementById('message-content');
    if (data.message) {
        msgEl.className = 'message-content';
        msgEl.textContent = data.message;
    } else {
        msgEl.className = 'message-content message-empty';
        msgEl.textContent = 'No additional message provided by the customer.';
    }
    
    document.getElementById('time-received').textContent = data.received;
    document.getElementById('val-source').textContent = data.source;
}

document.addEventListener('DOMContentLoaded', initReviewApp);
