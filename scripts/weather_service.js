    // WeatherService: Open-Meteo Free Weather API Integration
    // ============================================================
    const WeatherService = (() => {
      const LOCATIONS = {
        London: { name: "런던", lat: 51.5074, lon: -0.1278 },
        Oxford: { name: "옥스퍼드", lat: 51.7520, lon: -1.2577 },
        Paris: { name: "파리", lat: 48.8566, lon: 2.3522 },
        Versailles: { name: "베르사유", lat: 48.8049, lon: 2.1204 },
        Interlaken: { name: "인터라켄", lat: 46.6863, lon: 7.8632 },
        Jungfraujoch: { name: "융프라우요흐", lat: 46.5475, lon: 7.9822, elevation: 3454 },
        Grindelwald: { name: "그린델발트", lat: 46.6247, lon: 8.0345 },
        Zurich: { name: "취리히", lat: 47.3769, lon: 8.5417 },
        Incheon: { name: "서울/인천", lat: 37.4602, lon: 126.4407 }
      };

      const CARD_MAP = {
        "uk-d0": { city: "런던", loc: "London", date: "2026-09-10" },
        "uk-d1": { city: "런던", loc: "London", date: "2026-09-11" },
        "uk-d2": { city: "런던", loc: "London", date: "2026-09-12" },
        "uk-d3": { city: "옥스퍼드", loc: "Oxford", date: "2026-09-13" },
        "uk-d4": { city: "런던", loc: "London", date: "2026-09-14" },
        "uk-d5": { city: "런던➔파리", loc: "London", loc2: "Paris", date: "2026-09-15" },
        "paris-d1": { city: "파리", loc: "Paris", date: "2026-09-15" },
        "paris-d2": { city: "파리", loc: "Paris", date: "2026-09-16" },
        "paris-d3": { city: "베르사유", loc: "Versailles", date: "2026-09-17" },
        "paris-d4": { city: "파리➔스위스", loc: "Paris", loc2: "Interlaken", date: "2026-09-18" },
        "swiss-d8": { city: "인터라켄", loc: "Interlaken", date: "2026-09-18" },
        "swiss-d9": { city: "융프라우요흐", loc: "Jungfraujoch", date: "2026-09-19" },
        "swiss-d10": { city: "그린델발트", loc: "Grindelwald", date: "2026-09-20" },
        "swiss-d11": { city: "취리히", loc: "Zurich", date: "2026-09-21" },
        "swiss-d12": { city: "취리히", loc: "Zurich", date: "2026-09-22" },
        "swiss-d13": { city: "서울/인천", loc: "Incheon", date: "2026-09-23" }
      };

      const weatherData = {};
      let currentMode = SafeStorage.get("hm_weather_mode") || "live";
      const badgeOverrides = {};

      function getWmo(code) {
        const c = Number(code);
        if (c === 0) return { text: "맑음", icon: "wb_sunny", color: "text-amber-500" };
        if (c === 1) return { text: "대체로 맑음", icon: "sunny", color: "text-amber-500" };
        if (c === 2) return { text: "구름 조금", icon: "partly_cloudy_day", color: "text-sky-500" };
        if (c === 3) return { text: "흐림", icon: "cloud", color: "text-slate-500" };
        if (c === 45 || c === 48) return { text: "안개", icon: "foggy", color: "text-slate-400" };
        if (c >= 51 && c <= 55) return { text: "이슬비", icon: "rainy", color: "text-blue-500" };
        if (c >= 61 && c <= 65) return { text: "비", icon: "rainy", color: "text-blue-600" };
        if (c >= 71 && c <= 77) return { text: "눈", icon: "weather_snowy", color: "text-cyan-500" };
        if (c >= 80 && c <= 82) return { text: "소나기", icon: "shower", color: "text-indigo-500" };
        if (c >= 95) return { text: "뇌우", icon: "thunderstorm", color: "text-amber-600" };
        return { text: "맑음", icon: "wb_sunny", color: "text-amber-500" };
      }

      async function fetchLocationWeather(key, force) {
        const loc = LOCATIONS[key];
        if (!loc) return null;

        const cacheKey = "hm_weather_cache_" + key;
        const cacheTimeKey = "hm_weather_time_" + key;

        if (!force) {
          const cached = SafeStorage.get(cacheKey);
          const cacheTime = SafeStorage.get(cacheTimeKey);
          const now = Date.now();
          if (cached && cacheTime && (now - Number(cacheTime) < 15 * 60 * 1000)) {
            try {
              return JSON.parse(cached);
            } catch (_) {}
          }
        }

        try {
          let url = "https://api.open-meteo.com/v1/forecast?latitude=" + loc.lat + "&longitude=" + loc.lon + "&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min&forecast_days=16&timezone=auto";
          if (loc.elevation) {
            url += "&elevation=" + loc.elevation;
          }
          const res = await fetch(url);
          if (!res.ok) throw new Error("HTTP " + res.status);
          const data = await res.json();
          SafeStorage.set(cacheKey, JSON.stringify(data));
          SafeStorage.set(cacheTimeKey, String(Date.now()));
          return data;
        } catch (e) {
          console.warn("[WeatherService] Failed to fetch for " + key, e);
          const stale = SafeStorage.get(cacheKey);
          if (stale) {
            try { return JSON.parse(stale); } catch (_) {}
          }
          return null;
        }
      }

      async function fetchAll(force) {
        const keys = Object.keys(LOCATIONS);
        const promises = keys.map(k => fetchLocationWeather(k, force));
        const results = await Promise.all(promises);
        keys.forEach((k, idx) => {
          if (results[idx]) {
            weatherData[k] = results[idx];
          }
        });
        renderAll();
      }

      function renderAll() {
        renderHeaderWidgets();
        renderOverviewStrip();
        renderAllCards();
        updateToggleButtons();
      }

      function renderHeaderWidgets() {
        const uk = weatherData["London"];
        if (uk && uk.current) {
          const w = getWmo(uk.current.weather_code);
          const temp = Math.round(uk.current.temperature_2m * 10) / 10;
          const el = document.getElementById("header-weather-uk");
          if (el) {
            el.innerHTML = '<span class="material-symbols-outlined text-[14px] ' + w.color + '">' + w.icon + '</span><span class="font-bold text-primary">' + temp + '°C</span><span>· ' + w.text + '</span>';
          }
        }

        const fr = weatherData["Paris"];
        if (fr && fr.current) {
          const w = getWmo(fr.current.weather_code);
          const temp = Math.round(fr.current.temperature_2m * 10) / 10;
          const el = document.getElementById("header-weather-paris");
          if (el) {
            el.innerHTML = '<span class="material-symbols-outlined text-[14px] ' + w.color + '">' + w.icon + '</span><span class="font-bold text-primary">' + temp + '°C</span><span>· ' + w.text + '</span>';
          }
        }

        const sw = weatherData["Interlaken"];
        const jf = weatherData["Jungfraujoch"];
        if (sw && sw.current) {
          const w = getWmo(sw.current.weather_code);
          const temp = Math.round(sw.current.temperature_2m * 10) / 10;
          const jfTemp = (jf && jf.current) ? (Math.round(jf.current.temperature_2m * 10) / 10) + "°C" : "";
          const el = document.getElementById("header-weather-swiss");
          if (el) {
            let jfHtml = jfTemp ? '<span class="text-secondary font-bold ml-1">· 융프라우 ' + jfTemp + '</span>' : '';
            el.innerHTML = '<span class="material-symbols-outlined text-[14px] ' + w.color + '">' + w.icon + '</span><span class="font-bold text-primary">인터라켄 ' + temp + '°C · ' + w.text + '</span>' + jfHtml;
          }
        }
      }

      function renderOverviewStrip() {
        const uk = weatherData["London"];
        const fr = weatherData["Paris"];
        const sw = weatherData["Interlaken"];

        if (uk && uk.current) {
          const w = getWmo(uk.current.weather_code);
          const el = document.getElementById("home-weather-uk");
          const desc = document.getElementById("home-weather-desc-uk");
          if (el) el.innerHTML = '<span class="material-symbols-outlined text-[15px] ' + w.color + '">' + w.icon + '</span><span>' + (Math.round(uk.current.temperature_2m * 10) / 10) + '°C</span>';
          if (desc) desc.textContent = "실시간 · " + w.text;
        }

        if (fr && fr.current) {
          const w = getWmo(fr.current.weather_code);
          const el = document.getElementById("home-weather-paris");
          const desc = document.getElementById("home-weather-desc-paris");
          if (el) el.innerHTML = '<span class="material-symbols-outlined text-[15px] ' + w.color + '">' + w.icon + '</span><span>' + (Math.round(fr.current.temperature_2m * 10) / 10) + '°C</span>';
          if (desc) desc.textContent = "실시간 · " + w.text;
        }

        if (sw && sw.current) {
          const w = getWmo(sw.current.weather_code);
          const el = document.getElementById("home-weather-swiss");
          const desc = document.getElementById("home-weather-desc-swiss");
          if (el) el.innerHTML = '<span class="material-symbols-outlined text-[15px] ' + w.color + '">' + w.icon + '</span><span>' + (Math.round(sw.current.temperature_2m * 10) / 10) + '°C</span>';
          if (desc) desc.textContent = "실시간 · " + w.text;
        }

        const updated = document.getElementById("weather-last-updated");
        if (updated) {
          const d = new Date();
          const timeStr = String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0");
          updated.textContent = timeStr + " 실시간";
        }
      }

      function getCardDisplay(dayKey, mode) {
        const cfg = CARD_MAP[dayKey];
        if (!cfg) return null;

        const data = weatherData[cfg.loc];
        if (!data) return null;

        // Multi-destination cards (e.g. uk-d5 London->Paris, paris-d4 Paris->Swiss)
        if (cfg.loc2) {
          const data2 = weatherData[cfg.loc2];
          if (mode === "live") {
            if (data.current && data2 && data2.current) {
              const t1 = Math.round(data.current.temperature_2m);
              const t2 = Math.round(data2.current.temperature_2m);
              const w2 = getWmo(data2.current.weather_code);
              return {
                icon: w2.icon,
                color: w2.color,
                text: cfg.city + " 실시간 " + t1 + "°C ➔ " + t2 + "°C · " + w2.text,
                isLive: true
              };
            }
          } else {
            const times = data.daily ? data.daily.time : [];
            const times2 = data2 && data2.daily ? data2.daily.time : [];
            const idx = times.indexOf(cfg.date);
            const idx2 = times2.indexOf(cfg.date);
            if (idx !== -1 && idx2 !== -1 && data.daily.temperature_2m_max[idx] !== null) {
              const t1 = Math.round(data.daily.temperature_2m_max[idx]);
              const t2min = Math.round(data2.daily.temperature_2m_min[idx2]);
              const t2max = Math.round(data2.daily.temperature_2m_max[idx2]);
              const w2 = getWmo(data2.daily.weather_code[idx2]);
              return {
                icon: w2.icon,
                color: w2.color,
                text: cfg.city + " " + t1 + "°C ➔ " + t2min + "°C~" + t2max + "°C · " + w2.text,
                isLive: false
              };
            }
          }
        }

        if (mode === "live") {
          if (data.current) {
            const w = getWmo(data.current.weather_code);
            const temp = Math.round(data.current.temperature_2m * 10) / 10;
            const suffix = (dayKey === "swiss-d9") ? " (만년설/패딩)" : "";
            return {
              icon: w.icon,
              color: w.color,
              text: cfg.city + " 실시간 " + temp + "°C · " + w.text + suffix,
              isLive: true
            };
          }
        } else {
          const times = data.daily ? data.daily.time : [];
          const idx = times.indexOf(cfg.date);
          if (idx !== -1 && data.daily.temperature_2m_max[idx] !== null) {
            const tmin = Math.round(data.daily.temperature_2m_min[idx] * 10) / 10;
            const tmax = Math.round(data.daily.temperature_2m_max[idx] * 10) / 10;
            const w = getWmo(data.daily.weather_code[idx]);
            const suffix = (dayKey === "swiss-d9") ? " (만년설/패딩)" : "";
            return {
              icon: w.icon,
              color: w.color,
              text: cfg.city + " " + tmin + "°C~" + tmax + "°C · " + w.text + suffix,
              isLive: false
            };
          }
        }

        // Fallback to live if forecast is beyond 16 days
        if (data.current) {
          const w = getWmo(data.current.weather_code);
          const temp = Math.round(data.current.temperature_2m * 10) / 10;
          return {
            icon: w.icon,
            color: w.color,
            text: cfg.city + " 실시간 " + temp + "°C · " + w.text,
            isLive: true
          };
        }

        return null;
      }

      function renderCard(dayKey) {
        const textEl = document.getElementById("weather-text-" + dayKey);
        const iconEl = document.getElementById("weather-icon-" + dayKey);
        const badgeEl = document.getElementById("weather-badge-" + dayKey);
        if (!textEl || !iconEl) return;

        const mode = badgeOverrides[dayKey] || currentMode;
        const res = getCardDisplay(dayKey, mode);
        if (res) {
          textEl.textContent = res.text;
          iconEl.textContent = res.icon;
          iconEl.className = "material-symbols-outlined text-[14px] " + res.color;
          if (badgeEl) {
            if (res.isLive) {
              badgeEl.classList.add("text-primary", "font-medium");
            } else {
              badgeEl.classList.remove("text-primary", "font-medium");
            }
          }
        }
      }

      function renderAllCards() {
        Object.keys(CARD_MAP).forEach(k => renderCard(k));
      }

      function toggleMode() {
        currentMode = (currentMode === "live") ? "forecast" : "live";
        SafeStorage.set("hm_weather_mode", currentMode);
        for (const k in badgeOverrides) delete badgeOverrides[k];
        renderAllCards();
        updateToggleButtons();
      }

      function toggleBadge(dayKey) {
        const cur = badgeOverrides[dayKey] || currentMode;
        badgeOverrides[dayKey] = (cur === "live") ? "forecast" : "live";
        renderCard(dayKey);
      }

      function updateToggleButtons() {
        ["uk", "paris", "swiss"].forEach(c => {
          const btn = document.getElementById("weather-toggle-btn-" + c);
          if (btn) {
            if (currentMode === "live") {
              btn.innerHTML = '<span>⚡ 실시간 기온</span> <span class="text-[9.5px] opacity-75">⇋ 예보</span>';
              btn.classList.add("bg-primary/10", "text-primary");
            } else {
              btn.innerHTML = '<span>📅 일정별 예보</span> <span class="text-[9.5px] opacity-75">⇋ 실시간</span>';
              btn.classList.remove("bg-primary/10", "text-primary");
            }
          }
        });
      }

      return {
        init() {
          fetchAll(false);
        },
        refreshAll(force = true) {
          const updated = document.getElementById("weather-last-updated");
          if (updated) updated.textContent = "갱신 중...";
          fetchAll(force);
        },
        toggleMode,
        toggleBadge
      };
    })();
