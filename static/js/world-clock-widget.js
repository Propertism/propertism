(function () {
    function getFormatter(timeZone, includeSeconds, hour12) {
        return new Intl.DateTimeFormat("en-US", {
            timeZone: timeZone,
            hour: hour12 ? "numeric" : "2-digit",
            minute: "2-digit",
            second: includeSeconds ? "2-digit" : undefined,
            hour12: hour12,
            weekday: includeSeconds ? undefined : "short",
            month: includeSeconds ? undefined : "short",
            day: includeSeconds ? undefined : "numeric",
        });
    }

    function getParts(date, timeZone, includeSeconds, hour12) {
        const parts = getFormatter(timeZone, includeSeconds, hour12).formatToParts(date);

        function value(type) {
            const match = parts.find(function (part) {
                return part.type === type;
            });

            return match ? match.value : "";
        }

        return {
            hour: value("hour"),
            minute: value("minute"),
            second: value("second"),
            dayPeriod: value("dayPeriod"),
            weekday: value("weekday"),
            month: value("month"),
            day: value("day"),
        };
    }

    function buildCard(region) {
        const card = document.createElement("article");
        card.className = "world-clock-widget-card world-clock-widget-card--hybrid";
        card.dataset.region = region.region;
        card.dataset.timeZone = region.timeZone;
        card.title = "Local Time: " + region.city;

        // Minimal analog dial - no ticks, no second hand
        card.innerHTML = [
            '<div class="world-clock-widget-card-header">',
            '<span class="world-clock-widget-card-title"><span class="world-clock-widget-title-text">' + region.label + " (" + region.tzLabel + ')</span>' + (region.isoCode ? '<span class="fi fi-' + region.isoCode + ' world-clock-widget-title-flag" aria-hidden="true"></span>' : '') + '</span>',
            "</div>",
            '<div class="world-clock-widget-card-body">',
            '<div class="world-clock-widget-dial--mini" aria-hidden="true">',
            '<span class="world-clock-widget-hand-mini world-clock-widget-hand-hour-mini"></span>',
            '<span class="world-clock-widget-hand-mini world-clock-widget-hand-minute-mini"></span>',
            "</div>",
            '<div class="world-clock-widget-meta">',
            '<div class="world-clock-widget-time">',
            '<span class="world-clock-widget-hours">--</span><span class="world-clock-widget-separator">:</span><span class="world-clock-widget-minutes">--</span>',
            '<span class="world-clock-widget-meridiem">--</span>',
            "</div>",
            '<div class="world-clock-widget-inline-meta"><span class="world-clock-widget-date">--</span></div>',
            "</div>",
            "</div>",
        ].join("");

        return card;
    }

    function renderWidget(widget) {
        const configId = widget.dataset.configId;
        const configEl = configId ? document.getElementById(configId) : null;
        const grid = widget.querySelector("[data-world-clock-grid]");

        if (!configEl || !grid) {
            return [];
        }

        let regions = [];

        try {
            regions = JSON.parse(configEl.textContent || "[]");
        } catch (error) {
            console.error("WorldClockWidget config parse failed", error);
            return [];
        }

        if (!Array.isArray(regions) || !regions.length) {
            return [];
        }

        grid.innerHTML = "";
        const cards = regions.map(function (region) {
            const card = buildCard(region);
            grid.appendChild(card);
            return card;
        });

        return cards;
    }

    function updateCards(cards) {
        const now = new Date();

        cards.forEach(function (card) {
            const timeZone = card.dataset.timeZone;
            const digital = getParts(now, timeZone, false, true);
            const analog = getParts(now, timeZone, true, false);

            const hour = Number(analog.hour || 0);
            const minute = Number(analog.minute || 0);
            const second = Number(analog.second || 0);

            const hourRotation = ((hour % 12) * 30) + (minute * 0.5);
            const minuteRotation = minute * 6;
            const secondRotation = second * 6;

            const hourHand = card.querySelector(".world-clock-widget-hand-hour-mini, .world-clock-widget-hand-hour");
            const minuteHand = card.querySelector(".world-clock-widget-hand-minute-mini, .world-clock-widget-hand-minute");
            const secondHand = card.querySelector(".world-clock-widget-hand-second");
            const hoursEl = card.querySelector(".world-clock-widget-hours");
            const minutesEl = card.querySelector(".world-clock-widget-minutes");
            const meridiemEl = card.querySelector(".world-clock-widget-meridiem");
            const dateEl = card.querySelector(".world-clock-widget-date");

            if (hoursEl) hoursEl.textContent = digital.hour || "--";
            if (minutesEl) minutesEl.textContent = digital.minute || "--";
            if (meridiemEl) meridiemEl.textContent = (digital.dayPeriod || "").toLowerCase();
            if (dateEl) {
                dateEl.textContent = [digital.weekday, [digital.month, digital.day].filter(Boolean).join(" ")].filter(Boolean).join(", ");
            }

            if (hourHand) hourHand.style.transform = "translateX(-50%) rotate(" + hourRotation + "deg)";
            if (minuteHand) minuteHand.style.transform = "translateX(-50%) rotate(" + minuteRotation + "deg)";
        });
    }

    function updateAvailabilityBlocks() {
        const blocks = document.querySelectorAll("[data-footer-availability]");
        if (!blocks.length) {
            return;
        }

        const now = new Date();

        blocks.forEach(function (block) {
            const timeZone = block.dataset.tz || "Asia/Kolkata";
            const statusEl = block.querySelector("[data-footer-availability-status]");
            if (!statusEl) {
                return;
            }

            const parts = getParts(now, timeZone, false, false);
            const hour = Number(parts.hour || 0);
            const isOpen = hour >= 7 && hour < 23;

            statusEl.textContent = isOpen ? "Open Now" : "Closed Now";
            statusEl.dataset.state = isOpen ? "open" : "closed";
        });
    }

    function initWorldClockWidgets() {
        const widgets = Array.from(document.querySelectorAll("[data-world-clock-widget]"));
        const cards = widgets.length ? widgets.flatMap(renderWidget) : [];

        updateAvailabilityBlocks();

        if (!cards.length) {
            window.setInterval(function () {
                updateAvailabilityBlocks();
            }, 1000);
            return;
        }

        updateCards(cards);
        window.setInterval(function () {
            updateCards(cards);
            updateAvailabilityBlocks();
        }, 1000);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initWorldClockWidgets, { once: true });
    } else {
        initWorldClockWidgets();
    }
}());
