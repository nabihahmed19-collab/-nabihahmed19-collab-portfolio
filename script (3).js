(function () {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const CAT_VARS = {
    ml: "--cat-ml",
    dl: "--cat-dl",
    data: "--cat-data",
    genai: "--cat-genai",
    auto: "--cat-auto",
  };

  const CAT_ICONS = {
    ml: '<circle cx="8" cy="2.6" r="1.3"/><line x1="8" y1="3.9" x2="8" y2="6"/><line x1="8" y1="6" x2="3.6" y2="9"/><line x1="8" y1="6" x2="12.4" y2="9"/><circle cx="3.6" cy="10.3" r="1.3"/><circle cx="12.4" cy="10.3" r="1.3"/>',
    dl: '<circle cx="3" cy="4" r="1.2"/><circle cx="3" cy="12" r="1.2"/><circle cx="8" cy="8" r="1.2"/><circle cx="13" cy="4" r="1.2"/><circle cx="13" cy="12" r="1.2"/><line x1="3" y1="4" x2="8" y2="8"/><line x1="3" y1="12" x2="8" y2="8"/><line x1="13" y1="4" x2="8" y2="8"/><line x1="13" y1="12" x2="8" y2="8"/>',
    data: '<rect x="1.5" y="8" width="3" height="6" rx="0.5"/><rect x="6.5" y="3.5" width="3" height="10.5" rx="0.5"/><rect x="11.5" y="6" width="3" height="8" rx="0.5"/>',
    genai: '<path d="M8 1.3 L9.4 6.3 L14.4 7.7 L9.4 9.1 L8 14.1 L6.6 9.1 L1.6 7.7 L6.6 6.3 Z"/>',
    auto: '<path d="M3 8a5 5 0 0 1 8.6-3.5" fill="none"/><path d="M13 8a5 5 0 0 1-8.6 3.5" fill="none"/><path d="M11.6 2.5v2.5h-2.5" fill="none"/><path d="M4.4 13.5v-2.5h2.5" fill="none"/>',
  };

  function categoryIconSVG(catKey) {
    return `<span class="category-icon" style="color: var(${CAT_VARS[catKey]});"><svg viewBox="0 0 16 16" fill="currentColor" stroke="currentColor" stroke-width="1.3">${CAT_ICONS[catKey]}</svg></span>`;
  }

  function renderChart(chart, catKey) {
    if (!chart) return "";
    if (chart.type === "bar") {
      return `
        <div class="card-chart">
          <div class="chart-bar-track"><div class="chart-bar-fill" data-fill-to="${chart.value}"></div></div>
          <span class="chart-caption">${chart.caption}</span>
        </div>`;
    }
    if (chart.type === "compare") {
      const max = Math.max(...chart.values, 1);
      const heights = chart.values.map((v) => Math.max((v / max) * 100, 4));
      return `
        <div class="card-chart">
          <div class="chart-compare">
            <div class="chart-compare-col"><div class="chart-compare-bar" data-height-to="${heights[0]}"></div></div>
            <div class="chart-compare-col is-after"><div class="chart-compare-bar" data-height-to="${heights[1]}"></div></div>
          </div>
          <div class="chart-compare" style="height:auto; margin-top:-2px;">
            <div class="chart-compare-col"><span class="chart-compare-tick">${chart.labels[0]}</span></div>
            <div class="chart-compare-col"><span class="chart-compare-tick">${chart.labels[1]}</span></div>
          </div>
          <span class="chart-caption">${chart.caption}</span>
        </div>`;
    }
    return "";
  }

  function statusClass(status) {
    return status === "Live" ? "status-live" : "";
  }

  // ---------- Homepage: render projects grouped by category ----------
  const categoryBlocksEl = document.getElementById("categoryBlocks");
  if (categoryBlocksEl && typeof PROJECTS !== "undefined") {
    CATEGORIES.forEach((cat) => {
      const projectsInCat = PROJECTS.filter((p) => p.cat === cat.key);
      if (projectsInCat.length === 0) return;

      const block = document.createElement("div");
      block.className = "category-block reveal";

      const heading = document.createElement("div");
      heading.className = "category-heading";
      heading.innerHTML = `${categoryIconSVG(cat.key)}<h3>${cat.label}</h3>`;
      block.appendChild(heading);

      const grid = document.createElement("div");
      grid.className = "card-grid";

      projectsInCat.forEach((project) => {
        const card = document.createElement("a");
        card.className = "project-card";
        card.href = `${project.slug}.html`;
        card.style.setProperty("--card-accent", `var(${CAT_VARS[cat.key]})`);

        card.innerHTML = `
          <span class="card-status ${statusClass(project.status)}">${project.status}</span>
          <h4>${project.title}</h4>
          <p class="card-summary">${project.summary}</p>
          ${renderChart(project.chart, cat.key)}
          <p class="card-metric">${project.metric}</p>
          <span class="card-open">Open case study &rarr;</span>
        `;
        grid.appendChild(card);
      });

      block.appendChild(grid);
      categoryBlocksEl.appendChild(block);
    });
  }

  // ---------- Hero orbit animation (skills circling a center point) ----------
  const ORBIT_INNER = ["Python", "SQL", "Excel", "Power BI"];
  const ORBIT_OUTER = ["Machine Learning", "Deep Learning", "Gen AI", "Automation", "Data Analysis"];

  function buildOrbit(ringEl, items, radius, durationMs) {
    if (!ringEl) return;
    const n = items.length;
    items.forEach((label, i) => {
      const angle = (360 / n) * i;

      // Anchor: static rotate+translate to place this chip at its position on the ring.
      const chip = document.createElement("div");
      chip.className = "orbit-chip";
      chip.style.transform = `rotate(${angle}deg) translate(${radius}px)`;

      // Counter element: cancels the ring's rotation so the label stays upright.
      const counter = document.createElement("div");
      counter.className = "orbit-chip-counter";

      const labelWrap = document.createElement("div");
      labelWrap.className = "orbit-chip-label";
      labelWrap.innerHTML = `<span>${label}</span>`;

      counter.appendChild(labelWrap);
      chip.appendChild(counter);
      ringEl.appendChild(chip);

      if (!prefersReducedMotion && counter.animate) {
        counter.animate(
          [
            { transform: `rotate(${-angle}deg)` },
            { transform: `rotate(${-angle - 360}deg)` },
          ],
          { duration: durationMs, iterations: Infinity, easing: "linear" }
        );
      } else {
        counter.style.transform = `rotate(${-angle}deg)`;
      }
    });
  }

  const ringA = document.getElementById("orbitRingA");
  const ringB = document.getElementById("orbitRingB");
  if (ringA && ringB) {
    buildOrbit(ringA, ORBIT_INNER, 92, 26000);
    buildOrbit(ringB, ORBIT_OUTER, 150, 38000);
  }

  // ---------- Scroll-triggered reveal (generic, every section) ----------
  if (!prefersReducedMotion && "IntersectionObserver" in window) {
    const revealTargets = document.querySelectorAll(".reveal, .reveal-stagger");
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    revealTargets.forEach((el) => revealObserver.observe(el));

    // Journey path track (its own staggered line-draw animation)
    const pathTrack = document.getElementById("pathTrack");
    if (pathTrack) {
      const pathObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              pathTrack.classList.add("in-view");
              pathObserver.unobserve(pathTrack);
            }
          });
        },
        { threshold: 0.35 }
      );
      pathObserver.observe(pathTrack);
    }
  } else {
    document.querySelectorAll(".reveal, .reveal-stagger").forEach((el) => el.classList.add("in-view"));
    const pathTrack = document.getElementById("pathTrack");
    if (pathTrack) pathTrack.classList.add("in-view");
  }

  // ---------- Stats strip count-up ----------
  const statNumbers = document.querySelectorAll(".stat-number[data-count-to]");
  if (statNumbers.length) {
    const animateCount = (el) => {
      const target = parseInt(el.getAttribute("data-count-to"), 10);
      const suffix = el.getAttribute("data-suffix") || "";
      if (prefersReducedMotion) {
        el.textContent = target + suffix;
        return;
      }
      const duration = 1200;
      const start = performance.now();
      function tick(now) {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(eased * target) + suffix;
        if (progress < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    };
    if ("IntersectionObserver" in window) {
      const statObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              animateCount(entry.target);
              statObserver.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.5 }
      );
      statNumbers.forEach((el) => statObserver.observe(el));
    } else {
      statNumbers.forEach(animateCount);
    }
  }

  // ---------- Mini chart fill animation on project cards ----------
  const chartFills = document.querySelectorAll("[data-fill-to], [data-height-to]");
  if (chartFills.length && "IntersectionObserver" in window) {
    const chartObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            if (el.hasAttribute("data-fill-to")) {
              el.style.width = el.getAttribute("data-fill-to") + "%";
            }
            if (el.hasAttribute("data-height-to")) {
              el.style.height = el.getAttribute("data-height-to") + "%";
            }
            chartObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.3 }
    );
    chartFills.forEach((el) => chartObserver.observe(el));
  } else {
    chartFills.forEach((el) => {
      if (el.hasAttribute("data-fill-to")) el.style.width = el.getAttribute("data-fill-to") + "%";
      if (el.hasAttribute("data-height-to")) el.style.height = el.getAttribute("data-height-to") + "%";
    });
  }

  // ---------- Nav scroll-spy ----------
  const navLinks = document.querySelectorAll("#topnavLinks a[data-section]");
  if (navLinks.length && "IntersectionObserver" in window) {
    const sectionMap = {};
    navLinks.forEach((link) => {
      const id = link.getAttribute("data-section");
      const section = document.getElementById(id);
      if (section) sectionMap[id] = link;
    });
    const spyObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const id = entry.target.id;
          if (entry.isIntersecting && sectionMap[id]) {
            navLinks.forEach((l) => l.classList.remove("nav-active"));
            sectionMap[id].classList.add("nav-active");
          }
        });
      },
      { rootMargin: "-45% 0px -45% 0px" }
    );
    Object.keys(sectionMap).forEach((id) => {
      const el = document.getElementById(id);
      if (el) spyObserver.observe(el);
    });
  }
})();
