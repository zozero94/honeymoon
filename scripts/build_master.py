# -*- coding: utf-8 -*-
"""
build_master.py
Generates the complete, production-ready index.html and honeymoon-trip.html.
"""

import json
from generate_perfect_data import PINS, DAY_MAP_CONFIG, DAYS
from build_perfect_helpers import render_day_container, render_country_chips, render_accordion_item

# Group days by country
uk_days = ["uk-d0", "uk-d1", "uk-d2", "uk-d3", "uk-d4", "uk-d5"]
paris_days = ["paris-d1", "paris-d2", "paris-d3", "paris-d4"]
swiss_days = ["swiss-d8", "swiss-d9", "swiss-d10", "swiss-d11", "swiss-d12", "swiss-d13"]

# Render Day Containers
uk_containers_html = "\n".join([render_day_container(k, DAYS[k], is_default_visible=(k == "uk-d0")) for k in uk_days])
paris_containers_html = "\n".join([render_day_container(k, DAYS[k], is_default_visible=(k == "paris-d1")) for k in paris_days])
swiss_containers_html = "\n".join([render_day_container(k, DAYS[k], is_default_visible=(k == "swiss-d8")) for k in swiss_days])

# Render Day Chips
uk_chips_html = render_country_chips("uk", uk_days, "uk-d0")
paris_chips_html = render_country_chips("paris", paris_days, "paris-d1")
swiss_chips_html = render_country_chips("swiss", swiss_days, "swiss-d8")

# Render Accordions
uk_accordion_html = "\n".join([render_accordion_item(k, DAYS[k]) for k in uk_days])
paris_accordion_html = "\n".join([render_accordion_item(k, DAYS[k]) for k in paris_days])
swiss_accordion_html = "\n".join([render_accordion_item(k, DAYS[k]) for k in swiss_days])

# Load Open-Meteo Weather Service JS
with open("/Users/kakao/.gemini/antigravity/brain/7f9a6155-fc7e-41fc-9e51-2cae9c92c5c1/scratch/weather_service.js", "r", encoding="utf-8") as f:
    weather_service_js = f.read()

# Weather HTML snippets
overview_weather_html = """
        <!-- 현지 실시간 날씨 요약 위젯 (Open-Meteo 무료 API 연동) -->
        <div class="rounded-2xl bg-surface-container-lowest p-3.5 shadow-sm border border-border-subtle/40 space-y-2.5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5">
              <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span class="font-bold text-primary text-[13px]">여행지 현지 실시간 날씨</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 font-semibold">Open-Meteo 실시간</span>
            </div>
            <div class="flex items-center gap-1.5 text-[11px] text-on-surface-variant">
              <span id="weather-last-updated" class="text-[10px] opacity-80">날씨 수신 중...</span>
              <button type="button" onclick="WeatherService.refreshAll(true)" title="날씨 새로고침" class="p-1 rounded-md hover:bg-surface-container text-on-surface-variant hover:text-primary transition-colors flex items-center">
                <span class="material-symbols-outlined text-[14px]">refresh</span>
              </button>
            </div>
          </div>
          
          <div class="grid grid-cols-3 gap-2 text-center" id="overview-weather-cards">
            <!-- London -->
            <div onclick="jumpToDay('uk', 'uk-d0')" class="p-2.5 rounded-xl bg-surface-cream border border-border-subtle/40 cursor-pointer hover:border-primary/40 transition-colors">
              <span class="text-[11px] font-bold text-on-surface-variant block">🇬🇧 런던</span>
              <div id="home-weather-uk" class="text-[13px] font-bold text-primary flex items-center justify-center gap-1 mt-0.5">
                <span class="material-symbols-outlined text-[15px] text-amber-500 animate-spin">sync</span>
                <span>--°C</span>
              </div>
              <span id="home-weather-desc-uk" class="text-[10.5px] text-on-surface-variant block mt-0.5">확인 중</span>
            </div>
            <!-- Paris -->
            <div onclick="jumpToDay('paris', 'paris-d1')" class="p-2.5 rounded-xl bg-surface-cream border border-border-subtle/40 cursor-pointer hover:border-primary/40 transition-colors">
              <span class="text-[11px] font-bold text-on-surface-variant block">🇫🇷 파리</span>
              <div id="home-weather-paris" class="text-[13px] font-bold text-primary flex items-center justify-center gap-1 mt-0.5">
                <span class="material-symbols-outlined text-[15px] text-amber-500 animate-spin">sync</span>
                <span>--°C</span>
              </div>
              <span id="home-weather-desc-paris" class="text-[10.5px] text-on-surface-variant block mt-0.5">확인 중</span>
            </div>
            <!-- Swiss -->
            <div onclick="jumpToDay('swiss', 'swiss-d8')" class="p-2.5 rounded-xl bg-surface-cream border border-border-subtle/40 cursor-pointer hover:border-primary/40 transition-colors">
              <span class="text-[11px] font-bold text-on-surface-variant block">🇨🇭 스위스</span>
              <div id="home-weather-swiss" class="text-[13px] font-bold text-primary flex items-center justify-center gap-1 mt-0.5">
                <span class="material-symbols-outlined text-[15px] text-amber-500 animate-spin">sync</span>
                <span>--°C</span>
              </div>
              <span id="home-weather-desc-swiss" class="text-[10.5px] text-on-surface-variant block mt-0.5">확인 중</span>
            </div>
          </div>
        </div>
"""

uk_weather_bar_html = """
        <!-- London Live Weather Bar -->
        <div class="rounded-xl bg-surface-container-lowest p-3 shadow-xs border border-border-subtle/40 flex items-center justify-between text-[12px]">
          <div class="flex items-center gap-2">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span class="font-bold text-primary">🇬🇧 현지 실시간:</span>
            <span id="header-weather-uk" class="text-on-surface-variant font-medium flex items-center gap-1">
              <span class="material-symbols-outlined text-[14px] text-amber-500">wb_sunny</span>
              <span>런던 날씨 수신 중...</span>
            </span>
          </div>
          <div class="flex items-center gap-1.5">
            <button type="button" onclick="WeatherService.toggleMode()" id="weather-toggle-btn-uk" class="px-2 py-0.5 rounded-md bg-surface-container text-[11px] font-semibold text-on-surface hover:bg-surface-container-high transition-colors">
              ⚡ 실시간 기온
            </button>
            <button type="button" onclick="WeatherService.refreshAll(true)" title="날씨 새로고침" class="p-1 rounded-md text-on-surface-variant hover:text-primary transition-colors">
              <span class="material-symbols-outlined text-[15px]">refresh</span>
            </button>
          </div>
        </div>
"""

paris_weather_bar_html = """
        <!-- Paris Live Weather Bar -->
        <div class="rounded-xl bg-surface-container-lowest p-3 shadow-xs border border-border-subtle/40 flex items-center justify-between text-[12px]">
          <div class="flex items-center gap-2">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span class="font-bold text-primary">🇫🇷 현지 실시간:</span>
            <span id="header-weather-paris" class="text-on-surface-variant font-medium flex items-center gap-1">
              <span class="material-symbols-outlined text-[14px] text-amber-500">wb_sunny</span>
              <span>파리 날씨 수신 중...</span>
            </span>
          </div>
          <div class="flex items-center gap-1.5">
            <button type="button" onclick="WeatherService.toggleMode()" id="weather-toggle-btn-paris" class="px-2 py-0.5 rounded-md bg-surface-container text-[11px] font-semibold text-on-surface hover:bg-surface-container-high transition-colors">
              ⚡ 실시간 기온
            </button>
            <button type="button" onclick="WeatherService.refreshAll(true)" title="날씨 새로고침" class="p-1 rounded-md text-on-surface-variant hover:text-primary transition-colors">
              <span class="material-symbols-outlined text-[15px]">refresh</span>
            </button>
          </div>
        </div>
"""

swiss_weather_bar_html = """
        <!-- Swiss Live Weather Bar -->
        <div class="rounded-xl bg-surface-container-lowest p-3 shadow-xs border border-border-subtle/40 flex items-center justify-between text-[12px]">
          <div class="flex items-center gap-2">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span class="font-bold text-primary">🇨🇭 현지 실시간:</span>
            <span id="header-weather-swiss" class="text-on-surface-variant font-medium flex items-center gap-1">
              <span class="material-symbols-outlined text-[14px] text-amber-500">wb_sunny</span>
              <span>스위스 날씨 수신 중...</span>
            </span>
          </div>
          <div class="flex items-center gap-1.5">
            <button type="button" onclick="WeatherService.toggleMode()" id="weather-toggle-btn-swiss" class="px-2 py-0.5 rounded-md bg-surface-container text-[11px] font-semibold text-on-surface hover:bg-surface-container-high transition-colors">
              ⚡ 실시간 기온
            </button>
            <button type="button" onclick="WeatherService.refreshAll(true)" title="날씨 새로고침" class="p-1 rounded-md text-on-surface-variant hover:text-primary transition-colors">
              <span class="material-symbols-outlined text-[15px]">refresh</span>
            </button>
          </div>
        </div>
"""

# Calendar Days Generation (September 2026: Sep 1 is Tuesday -> empty slot for Mon)
# September 1 to 30:
cal_items = []
# 1 blank for Monday Aug 31
cal_items.append('<div class="py-1 text-on-surface-variant/30 text-center font-bold text-[12px]"></div>')

for d in range(1, 31):
    # Days 10 to 23 are trip days
    if 10 <= d <= 23:
        if 10 <= d <= 14:
            cKey = "uk"
            dKey = f"uk-d{d-10}"
            dot_color = "bg-[#1D4ED8]" # 로열 블루 (런던)
        elif d == 15:
            cKey = "paris"
            dKey = "paris-d1"
            dot_color = "bg-[#E11D48]" # 비비드 로맨틱 로즈 (파리 도착)
        elif 16 <= d <= 17:
            cKey = "paris"
            dKey = f"paris-d{d-14}"
            dot_color = "bg-[#E11D48]" # 비비드 로맨틱 로즈 (파리)
        elif d == 18:
            cKey = "swiss"
            dKey = "swiss-d8"
            dot_color = "bg-[#059669]" # 알프스 에메랄드 그린 (스위스 도착)
        elif 19 <= d <= 22:
            cKey = "swiss"
            dKey = f"swiss-d{d-10}"
            dot_color = "bg-[#059669]" # 알프스 에메랄드 그린 (스위스)
        else: # 23
            cKey = "swiss"
            dKey = "swiss-d13"
            dot_color = "bg-[#059669]" # 알프스 에메랄드 그린 (귀국)
            
        cal_items.append(f'''
        <button type="button" onclick="jumpToDay('{cKey}', '{dKey}')" class="cal-day-btn py-1 rounded-lg bg-surface-cream text-primary flex flex-col items-center justify-center text-[12px] font-bold border border-border-subtle/30 shadow-2xs hover:bg-surface-container active:scale-95 transition-all">
          <span>{d}</span>
          <span class="w-2 h-2 rounded-full {dot_color} -mt-0.5 shadow-xs"></span>
        </button>
        ''')
    else:
        cal_items.append(f'''
        <div class="py-1 text-on-surface-variant/40 text-center font-medium text-[12px]">
          <span>{d}</span>
        </div>
        ''')

calendar_grid_html = "\n".join(cal_items)

# Construct full HTML
full_html = f'''<!DOCTYPE html>
<html lang="ko" class="h-full bg-background-light">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
  <title>Grand Tour · 런던·파리·스위스 허니문 13박 14일</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet"/>
  <!-- Optimized Material Symbols (~40KB with display=swap) -->
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap" rel="stylesheet"/>
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  
  <!-- Tailwind Play CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            primary: {{ DEFAULT: '#1B2A4A', container: '#243B6A' }},
            secondary: {{ DEFAULT: '#4A5D4E', container: '#687F6D' }},
            'london-crimson': '#8B2635',
            'parisian-rose': '#A35064',
            'swiss-red': '#A8201A',
            'canvas-ivory': '#FAFAF7',
            'surface-cream': '#F4F1EA',
            'surface-container-lowest': '#FFFFFF',
            'surface-container': '#EFECE6',
            'surface-container-high': '#E5E1D8',
            'on-surface': '#2C3539',
            'on-surface-variant': '#5A656B',
            'on-primary': '#FFFFFF',
            'border-subtle': '#D8D4CC'
          }},
          spacing: {{
            'space-xs': '4px',
            'space-sm': '8px',
            'space-md': '12px',
            'space-lg': '16px',
            'space-xl': '24px'
          }}
        }}
      }}
    }};
  </script>

  <style>
    /* Safe Area Insets & Layout Shell */
    :root {{
      --sat: env(safe-area-inset-top, 0px);
      --sab: env(safe-area-inset-bottom, 0px);
    }}
    .pt-safe {{
      padding-top: max(8px, env(safe-area-inset-top, 0px)) !important;
    }}
    .pb-safe {{
      padding-bottom: max(12px, env(safe-area-inset-bottom, 0px)) !important;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #e5e8ef;
      margin: 0;
      padding: 0;
      color: #2C3539;
      -webkit-font-smoothing: antialiased;
    }}

    #app-shell {{
      width: 100%;
      max-width: 480px;
      background-color: #FAFAF7;
      min-height: 100vh;
      min-height: 100dvh;
      position: relative;
      box-shadow: 0 10px 40px rgba(0,0,0,0.12);
      overflow-x: hidden;
      display: flex;
      flex-direction: column;
      margin-left: auto;
      margin-right: auto;
    }}

    /* Fixed Navigation Bar centered on desktop without subpixel blur */
    nav.fixed {{
      left: 0 !important;
      right: 0 !important;
      margin-left: auto !important;
      margin-right: auto !important;
      width: 100% !important;
      max-width: 480px !important;
    }}

    /* Dynamic bottom padding for main */
    main {{
      padding-bottom: calc(6rem + env(safe-area-inset-bottom, 0px)) !important;
    }}

    /* Horizontal Scroller touch settings */
    #scroller-uk, #scroller-paris, #scroller-swiss {{
      overscroll-behavior-x: contain;
      -webkit-overflow-scrolling: touch;
    }}

    /* Offline resilience & critical utilities */
    .hidden {{ display: none !important; }}
    .no-scrollbar::-webkit-scrollbar {{ display: none; }}
    .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
    
    .leaflet-pane img, .leaflet-tile, .leaflet-marker-icon, .leaflet-marker-shadow, .leaflet-tile-container img {{
      max-width: none !important;
      max-height: none !important;
    }}
  </style>
</head>

<body class="min-h-screen">
  <div id="app-shell">

    <!-- Top Sticky Header -->
    <header class="sticky top-0 z-40 bg-canvas-ivory/95 backdrop-blur-md border-b border-border-subtle/40 px-4 py-3 pt-safe">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white shadow-xs">
            <span class="material-symbols-outlined text-[18px]">travel_explore</span>
          </div>
          <div>
            <h1 class="font-bold text-[14.5px] text-primary tracking-tight leading-none font-serif">Grand Tour</h1>
            <div class="flex items-center gap-1.5 mt-0.5">
              <span id="dday-badge" class="px-1.5 py-0.5 rounded bg-london-crimson text-white text-[10px] font-extrabold tracking-wider">D-DAY</span>
              <span class="text-[11px] text-on-surface-variant font-medium">9.10 ➔ 9.23</span>
            </div>
          </div>
        </div>

        <!-- Quick Action Buttons -->
        <div class="flex items-center gap-1.5">
          <button type="button" onclick="openSosModal()" title="비상 연락처 (대사관/긴급/병원)" class="flex items-center gap-1 px-2.5 py-1.5 rounded-full bg-london-crimson text-white hover:bg-london-crimson/90 active:scale-95 transition-all shadow-xs text-[11.5px] font-bold">
            <span class="material-symbols-outlined text-[15px]">emergency</span>
            <span>SOS</span>
          </button>
          <button type="button" onclick="shareTrip()" title="일정 공유하기" class="p-2 rounded-full bg-surface-cream text-on-surface hover:bg-surface-container active:scale-95 transition-all border border-border-subtle/40">
            <span class="material-symbols-outlined text-[19px]">share</span>
          </button>
          <button type="button" onclick="openVouchersModal()" title="확정 바우처 모아보기" class="flex items-center gap-1 px-2.5 py-1.5 rounded-full bg-primary text-white hover:bg-primary/90 active:scale-95 transition-all shadow-xs text-[12px] font-bold">
            <span class="material-symbols-outlined text-[16px]">bookmark</span>
            <span>바우처</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Screens Container -->
    <main class="flex-1 px-4 py-4 space-y-5">

      <!-- ============================================================ -->
      <!-- SCREEN 1: HOME (OVERVIEW)                                    -->
      <!-- ============================================================ -->
      <section id="screen-home" class="screen-page space-y-4">
        
        <!-- Hero Summary Card -->
        <div class="rounded-2xl bg-gradient-to-br from-primary via-[#243B6A] to-[#1B2A4A] p-5 text-white shadow-md space-y-3.5 relative overflow-hidden">
          <div class="absolute -right-4 -bottom-4 w-32 h-32 bg-white/5 rounded-full blur-xl pointer-events-none"></div>
          
          <div class="flex items-center justify-between">
            <span class="px-2.5 py-1 rounded-full bg-white/15 text-white/90 text-[11px] font-bold uppercase tracking-wider backdrop-blur-xs">Honeymoon 13박 14일</span>
            <span class="text-white/80 text-[12px] font-medium flex items-center gap-1">
              <span class="material-symbols-outlined text-[15px]">favorite</span>
              신혼여행
            </span>
          </div>

          <div>
            <h2 class="text-[20px] font-bold font-serif leading-tight">런던 · 파리 · 스위스 알프스</h2>
            <p class="text-white/80 text-[12.5px] mt-1">2026.09.10 (목) ➔ 2026.09.23 (수)</p>
          </div>

          <!-- Key Metrics Grid -->
          <div class="grid grid-cols-3 gap-2 pt-2 border-t border-white/15">
            <div class="rounded-xl bg-white/10 p-2 text-center backdrop-blur-xs">
              <span class="block text-[10px] text-white/70">숙소 예약</span>
              <span class="text-[13px] font-bold text-white">5곳 완료</span>
            </div>
            <div class="rounded-xl bg-white/10 p-2 text-center backdrop-blur-xs">
              <span class="block text-[10px] text-white/70">초고속열차</span>
              <span class="text-[13px] font-bold text-white">2편 확정</span>
            </div>
            <div class="rounded-xl bg-white/10 p-2 text-center backdrop-blur-xs">
              <span class="block text-[10px] text-white/70">핵심 투어</span>
              <span class="text-[13px] font-bold text-white">6곳 확정</span>
            </div>
          </div>
        </div>

        {overview_weather_html}

        <!-- 9월 캘린더 인터랙티브 그리드 -->
        <div class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-primary text-[14px] flex items-center gap-1.5">
              <span class="material-symbols-outlined text-[17px] text-primary">calendar_month</span>
              <span>2026년 9월 여정 달력</span>
            </h3>
            <span class="text-[11px] text-on-surface-variant font-medium">날짜 탭하여 이동</span>
          </div>

          <!-- Day Labels -->
          <div class="grid grid-cols-7 gap-1 text-center font-bold text-[11px] text-on-surface-variant pb-1 border-b border-border-subtle/30">
            <span class="text-london-crimson">일</span>
            <span>월</span>
            <span>화</span>
            <span>수</span>
            <span>목</span>
            <span>금</span>
            <span class="text-primary">토</span>
          </div>

          <!-- 30 Calendar Days Grid -->
          <div class="grid grid-cols-7 gap-1">
            {calendar_grid_html}
          </div>

          <!-- Legend -->
          <div class="flex items-center justify-center gap-3 pt-2 text-[11px] text-on-surface-variant border-t border-border-subtle/30">
            <span class="flex items-center gap-1.5 font-medium">
              <span class="w-2.5 h-2.5 rounded-full bg-[#1D4ED8] shadow-xs"></span> 런던(5박)
            </span>
            <span class="flex items-center gap-1.5 font-medium">
              <span class="w-2.5 h-2.5 rounded-full bg-[#E11D48] shadow-xs"></span> 파리(3박)
            </span>
            <span class="flex items-center gap-1.5 font-medium">
              <span class="w-2.5 h-2.5 rounded-full bg-[#059669] shadow-xs"></span> 스위스(5박)
            </span>
          </div>
        </div>

        <!-- 3 Country Fast Switch Cards -->
        <div class="space-y-2.5">
          <h3 class="font-bold text-primary text-[14px] px-1">국가별 일정 바로가기</h3>

          <!-- UK Card -->
          <div onclick="switchMainTab('uk')" class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 cursor-pointer hover:border-[#1D4ED8]/40 transition-all flex items-center justify-between active:scale-[0.99]">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-[#1D4ED8]/10 text-[#1D4ED8] flex items-center justify-center font-bold text-[18px]">
                🇬🇧
              </div>
              <div>
                <div class="flex items-center gap-1.5">
                  <h4 class="font-bold text-primary text-[14.5px]">영국 런던</h4>
                  <span class="px-1.5 py-0.2 rounded bg-surface-cream text-[#1D4ED8] font-bold text-[10.5px]">5박 6일</span>
                </div>
                <p class="text-[12px] text-on-surface-variant mt-0.5">소호 에어비앤비 · 런던아이 · 빅벤 스냅 · 옥스퍼드</p>
              </div>
            </div>
            <span class="material-symbols-outlined text-on-surface-variant text-[20px]">chevron_right</span>
          </div>

          <!-- Paris Card -->
          <div onclick="switchMainTab('paris')" class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 cursor-pointer hover:border-[#E11D48]/40 transition-all flex items-center justify-between active:scale-[0.99]">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-[#E11D48]/10 text-[#E11D48] flex items-center justify-center font-bold text-[18px]">
                🇫🇷
              </div>
              <div>
                <div class="flex items-center gap-1.5">
                  <h4 class="font-bold text-primary text-[14.5px]">프랑스 파리</h4>
                  <span class="px-1.5 py-0.2 rounded bg-surface-cream text-[#E11D48] font-bold text-[10.5px]">3박 4일</span>
                </div>
                <p class="text-[12px] text-on-surface-variant mt-0.5">15구 에펠뷰 · 루브르(14:30) · 베르사유(11:30)</p>
              </div>
            </div>
            <span class="material-symbols-outlined text-on-surface-variant text-[20px]">chevron_right</span>
          </div>

          <!-- Swiss Card -->
          <div onclick="switchMainTab('swiss')" class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 cursor-pointer hover:border-[#059669]/40 transition-all flex items-center justify-between active:scale-[0.99]">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-[#059669]/10 text-[#059669] flex items-center justify-center font-bold text-[18px]">
                🇨🇭
              </div>
              <div>
                <div class="flex items-center gap-1.5">
                  <h4 class="font-bold text-primary text-[14.5px]">스위스 알프스</h4>
                  <span class="px-1.5 py-0.2 rounded bg-surface-cream text-[#059669] font-bold text-[10.5px]">5박 6일</span>
                </div>
                <p class="text-[12px] text-on-surface-variant mt-0.5">운터젠 · 융프라우(신라면) · 피르스트 · 선스타 · 취리히</p>
              </div>
            </div>
            <span class="material-symbols-outlined text-on-surface-variant text-[20px]">chevron_right</span>
          </div>
        </div>

        <!-- Master Checklist Card -->
        <div class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 space-y-2.5">
          <div class="flex items-center justify-between">
            <h3 class="font-bold text-primary text-[14px] flex items-center gap-1.5">
              <span class="material-symbols-outlined text-secondary text-[17px]">checklist</span>
              <span>허니문 필수 확정 예약 점검</span>
            </h3>
            <span class="text-[11px] text-on-surface-variant font-medium">자동 저장</span>
          </div>

          <div class="space-y-1 divide-y divide-border-subtle/30 text-[12.5px]">
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-hex" data-key="uk_hex" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>🚅 히드로 익스프레스 직통 (JNR875059)</span>
              <a href="https://www.klook.com/ko/experiences/booking_detail/?guid=5583938439&bookingNo=JNR875059&sub_category_id=171" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline ml-auto">클룩 예약 ↗</a>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-snap" data-key="uk_snap" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>📷 런던 허니문 스냅 (9/11 08:30 빅벤 4번 출구)</span>
              <a href="https://www.myrealtrip.com/reservations/EXP-20260809-00014349" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline ml-auto">예약 확인 ↗</a>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-eye" data-key="uk_eye" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>🎡 런던아이 10:30 패스트트랙 (QKZ212209)</span>
              <a href="https://www.klook.com/ko/experiences/booking_detail/?guid=5583382053&bookingNo=QKZ212209&sub_category_id=1" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline ml-auto">클룩 예약 ↗</a>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-stpaul" data-key="uk_stpaul" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>⛪ 세인트폴 대성당 13:30 (EYY349639)</span>
              <a href="https://www.klook.com/ko/experiences/booking_detail/?guid=5583448316&bookingNo=EYY349639&sub_category_id=1" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline ml-auto">클룩 예약 ↗</a>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-ox-christ" data-key="ox_christ" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>🏰 옥스퍼드 크라이스트 처치 (14:30 · D83G8RWS5)</span>
              <a href="./vouchers/christ_church_ticket.png" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline ml-auto">QR 티켓 ↗</a>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-eurostar" data-key="uk_eurostar" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>🚅 유로스타 9032 (9/15 13:31 · 주문 5432599190)</span>
              <a href="https://www.klook.com/ko/ptp/order-details/?order_no=5432599190" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline ml-auto">클룩 주문 ↗</a>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-louvre" data-key="fr_louvre" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>🏛️ 루브르 박물관 (9/16 14:30 슬롯)</span>
              <a href="https://www.klook.com/ko/voucher-new/8c58a9bc-5acc-41ad-4040-7ba6a90ebbf4?lang=ko_KR&spm=BookingDetail.ViewVoucher&clickId=0efbcca78b" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline ml-auto">바우처 ↗</a>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-versailles" data-key="fr_versailles" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>🏰 베르사유 궁전 (9/17 11:30 · ZKN582328)</span>
              <div class="ml-auto flex items-center gap-1.5">
                <a href="https://www.klook.com/ko/experiences/booking_detail/?guid=5583092533&bookingNo=ZKN582328&sub_category_id=1" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline">예약 상세 ↗</a>
                <a href="https://www.klook.com/klvoucher/REZJbmVJUXhSV2V6UjZCcDl2TXNDdkZHTjN5cVhaaVYrb05HdGpEdXRpbnNWTmwreDJVaU5XZ0VNelpEczNxemZvbU5lRVRPSnNXa0hla3dTUHh1cHFpcjk2K21yaXZmRllLY2czdlo0Z0k9.pdf?spm=BookingDetail.ViewVoucher&clickId=53426a21ce" target="_blank" rel="noopener noreferrer" class="text-on-surface-variant text-xs underline">PDF ↗</a>
              </div>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-tgv" data-key="tgv_lyria" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>🚄 TGV Lyria 9211 (9/18 10:22 리옹역 발차)</span>
              <a href="https://www.klook.com/ko/add-upcoming-trip/?id=2ac7ebb5-7712-4e8e-4fc6-5c8ad540c6ad&utm_campaign=platform-share&utm_content=platform%3Dapp_pagespm%3DShareBookingPreview_textversion%3D1_shareid%3Dcfdf8d05-e37c-40b9-b6b6-f68d6c0fb60f&utm_medium=kakao-talk&utm_source=kakao" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline ml-auto">클룩 예약 ↗</a>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-dongshin" data-key="sw_dongshin" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>📄 동신항운 신라면 할인쿠폰 종이 인쇄 완료 ✅</span>
              <a href="https://www.jungfrau.co.kr" target="_blank" rel="noopener noreferrer" class="text-secondary font-bold text-xs underline ml-auto">쿠폰 안내 ↗</a>
            </label>
            <label class="flex items-center gap-2 py-1.5 cursor-pointer">
              <input type="checkbox" id="chk-all-swisspass" data-key="sw_pass" checked class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
              <span>🎫 스위스 트래블 패스 4일권 (9/18~9/21)</span>
              <span class="text-secondary font-bold text-xs ml-auto">연속권</span>
            </label>
          </div>
        </div>

      </section>

      <!-- ============================================================ -->
      <!-- SCREEN 2: UK (LONDON)                                        -->
      <!-- ============================================================ -->
      <section id="screen-uk" class="screen-page space-y-4 hidden">
        
        <!-- London Hero Stay Card -->
        <div class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 space-y-2">
          <div class="flex items-center justify-between">
            <span class="px-2 py-0.5 rounded-full bg-london-crimson/10 text-london-crimson font-label-caps text-[11px] font-bold">5박 베이스캠프</span>
            <a href="https://www.airbnb.co.kr/trips/v1/1677481706963156774" target="_blank" rel="noopener noreferrer" class="text-london-crimson text-[11.5px] font-bold">
              예약 확인 ↗
            </a>
          </div>
          <h3 class="font-title-lg text-primary font-bold text-[16px]">소호 플랫 에어비앤비 (Dean St)</h3>
          <p class="text-[12px] text-on-surface-variant leading-relaxed">
            체크인: 9/10 (목) 19:30 · 체크아웃: 9/15 (화) 12:00 (5박)<br/>
            피카딜리 서커스 역 도보 3분 · 런던 튜브 및 맛집 접근성 최고
          </p>
          <div class="pt-1">
            <a href="https://www.google.com/maps/search/?api=1&query=Dean+St,+Soho,+London" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-[11.5px] text-primary font-semibold">
              <span class="material-symbols-outlined text-[14px]">pin_drop</span>
              <span>구글맵에서 숙소 위치 확인</span>
            </a>
          </div>
        </div>

        {uk_weather_bar_html}

        <!-- London Day Chips Bar -->
        <div id="scroller-uk" class="flex gap-2 overflow-x-auto no-scrollbar py-1">
          {uk_chips_html}
        </div>

        <!-- London Day Containers -->
        {uk_containers_html}

        <!-- London Accordion Full Briefing -->
        <div class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 space-y-2.5">
          <h4 class="font-bold text-primary text-[14px] flex items-center gap-1.5">
            <span class="material-symbols-outlined text-london-crimson text-[17px]">format_list_bulleted</span>
            <span>런던 5박 6일 전 일정 브리핑 펼쳐보기</span>
          </h4>
          <div class="space-y-1.5">
            {uk_accordion_html}
          </div>
        </div>

      </section>

      <!-- ============================================================ -->
      <!-- SCREEN 3: PARIS                                              -->
      <!-- ============================================================ -->
      <section id="screen-paris" class="screen-page space-y-4 hidden">
        
        <!-- Paris Hero Stay Card -->
        <div class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 space-y-2">
          <div class="flex items-center justify-between">
            <span class="px-2 py-0.5 rounded-full bg-parisian-rose/10 text-parisian-rose font-label-caps text-[11px] font-bold">3박 베이스캠프</span>
            <a href="https://www.airbnb.co.kr/trips/v1/reservation-details/ro/RESERVATION2_CHECKIN/HMJNDQRQSC" target="_blank" rel="noopener noreferrer" class="text-parisian-rose text-[11.5px] font-bold">
              예약 확인 ↗
            </a>
          </div>
          <h3 class="font-title-lg text-primary font-bold text-[16px]">파리 15구 에펠탑 인근 숙소 (Allée Joseph Récamier)</h3>
          <p class="text-[12px] text-on-surface-variant leading-relaxed">
            체크인: 9/15 (화) 18:00 · 체크아웃: 9/18 (금) 09:30 (3박)<br/>
            주소: 10 Allée Joseph Récamier, 75015 Paris · 샹 드 마르스 도보권
          </p>
          <div class="pt-1">
            <a href="https://www.google.com/maps/search/?api=1&query=10+All.+Joseph+Recamier%2C+75015+Paris" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-[11.5px] text-primary font-semibold">
              <span class="material-symbols-outlined text-[14px]">pin_drop</span>
              <span>구글맵에서 파리 숙소 위치 확인</span>
            </a>
          </div>
        </div>

        <!-- Paris Confirmed Slots Banner -->
        <div class="p-3 rounded-xl bg-gradient-to-r from-parisian-rose/15 to-parisian-rose/5 border border-parisian-rose/30 space-y-1.5">
          <span class="px-1.5 py-0.5 rounded bg-parisian-rose text-white text-[10px] font-bold">파리 핵심 예약 확정</span>
          <div class="grid grid-cols-2 gap-2 pt-1 text-[12px]">
            <a href="https://www.klook.com/ko/voucher-new/8c58a9bc-5acc-41ad-4040-7ba6a90ebbf4?lang=ko_KR&spm=BookingDetail.ViewVoucher&clickId=0efbcca78b" target="_blank" rel="noopener noreferrer" class="p-2 rounded-lg bg-surface-container-lowest shadow-2xs font-semibold text-primary flex items-center justify-between">
              <span>🏛️ 루브르 9/16 14:30</span>
              <span class="text-parisian-rose text-[11px]">바우처 ↗</span>
            </a>
            <a href="https://www.klook.com/klvoucher/REZJbmVJUXhSV2V6UjZCcDl2TXNDdkZHTjN5cVhaaVYrb05HdGpEdXRpbnNWTmwreDJVaU5XZ0VNelpEczNxemZvbU5lRVRPSnNXa0hla3dTUHh1cHFpcjk2K21yaXZmRllLY2czdlo0Z0k9.pdf?spm=BookingDetail.ViewVoucher&clickId=53426a21ce" target="_blank" rel="noopener noreferrer" class="p-2 rounded-lg bg-surface-container-lowest shadow-2xs font-semibold text-primary flex items-center justify-between">
              <span>🏰 베르사유 9/17 11:30</span>
              <span class="text-parisian-rose text-[11px]">PDF ↗</span>
            </a>
          </div>
        </div>

        {paris_weather_bar_html}

        <!-- Paris Day Chips Bar -->
        <div id="scroller-paris" class="flex gap-2 overflow-x-auto no-scrollbar py-1">
          {paris_chips_html}
        </div>

        <!-- Paris Day Containers -->
        {paris_containers_html}

        <!-- Paris Accordion Full Briefing -->
        <div class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 space-y-2.5">
          <h4 class="font-bold text-primary text-[14px] flex items-center gap-1.5">
            <span class="material-symbols-outlined text-parisian-rose text-[17px]">format_list_bulleted</span>
            <span>파리 3박 4일 전 일정 브리핑 펼쳐보기</span>
          </h4>
          <div class="space-y-1.5">
            {paris_accordion_html}
          </div>
        </div>

      </section>

      <!-- ============================================================ -->
      <!-- SCREEN 4: SWISS                                              -->
      <!-- ============================================================ -->
      <section id="screen-swiss" class="screen-page space-y-4 hidden">
        
        <!-- Swiss 3 Basecamps Relay Card -->
        <div class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 space-y-2.5">
          <div class="flex items-center justify-between">
            <span class="px-2 py-0.5 rounded-full bg-secondary/10 text-secondary font-label-caps text-[11px] font-bold">5박 3대 거점 릴레이</span>
            <span class="text-secondary text-[11px] font-bold">스위스 트래블 패스 4일권</span>
          </div>
          
          <div class="space-y-2 text-[12.5px]">
            <div class="p-2 rounded-xl bg-surface-cream border border-border-subtle/30 flex items-center justify-between">
              <div>
                <span class="font-bold text-primary">1. 인터라켄 운터젠 숙소</span>
                <span class="block text-[11px] text-on-surface-variant">9/18~9/20 (2박) · Obere Gasse · 게스트 카드 무료</span>
              </div>
              <div class="flex items-center gap-2">
                <a href="https://www.airbnb.co.kr/trips/v1/1681698459825419428" target="_blank" rel="noopener noreferrer" class="text-secondary font-bold text-[11px]">에어비앤비 ↗</a>
                <a href="https://www.google.com/maps/search/?api=1&query=Obere+Gasse%2C+Unterseen%2C+Bern+3800" target="_blank" rel="noopener noreferrer" class="text-on-surface-variant text-[11px]">구글맵 ↗</a>
              </div>
            </div>

            <div class="p-2 rounded-xl bg-surface-cream border border-border-subtle/30 flex items-center justify-between">
              <div>
                <span class="font-bold text-primary">2. 그린델발트 선스타 호텔</span>
                <span class="block text-[11px] text-on-surface-variant">9/20~9/21 (1박) · 아이거 북벽 뷰 & 스파 발코니</span>
              </div>
              <div class="flex items-center gap-2">
                <a href="./vouchers/sunstar_hotel.pdf" target="_blank" rel="noopener noreferrer" class="text-secondary font-bold text-[11px]">바우처 PDF ↗</a>
                <a href="https://www.google.com/maps/search/?api=1&query=Sunstar+Hotel+Grindelwald" target="_blank" rel="noopener noreferrer" class="text-on-surface-variant text-[11px]">구글맵 ↗</a>
              </div>
            </div>

            <div class="p-2 rounded-xl bg-surface-cream border border-border-subtle/30 flex items-center justify-between">
              <div>
                <span class="font-bold text-primary">3. 취리히 중앙역 MANY'S 숙소</span>
                <span class="block text-[11px] text-on-surface-variant">9/21~9/22 (1박) · 구시가지 & 공항철도 12분</span>
              </div>
              <div class="flex items-center gap-2">
                <a href="./vouchers/zurich_stay.pdf" target="_blank" rel="noopener noreferrer" class="text-secondary font-bold text-[11px]">바우처 PDF ↗</a>
                <a href="https://www.google.com/maps/search/?api=1&query=MANY%27S+historical+city+central+APARTMENTS" target="_blank" rel="noopener noreferrer" class="text-on-surface-variant text-[11px]">구글맵 ↗</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Swiss Pass & Coupon Banner -->
        <div class="p-3 rounded-xl bg-gradient-to-r from-secondary/15 to-secondary/5 border border-secondary/30 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-secondary text-[22px]">ramen_dining</span>
            <div>
              <span class="font-bold text-primary text-[12.5px] block">동신항운 신라면 종이쿠폰 준비 완료 ✅</span>
              <span class="text-[11px] text-on-surface-variant">융프라우 정상 무료 컵라면 교환권</span>
            </div>
          </div>
          <a href="https://www.jungfrau.co.kr" target="_blank" rel="noopener noreferrer" class="px-2.5 py-1 rounded bg-secondary text-white text-[11px] font-bold hover:bg-secondary/90">
            쿠폰 안내 ↗
          </a>
        </div>

        {swiss_weather_bar_html}

        <!-- Swiss Day Chips Bar -->
        <div id="scroller-swiss" class="flex gap-2 overflow-x-auto no-scrollbar py-1">
          {swiss_chips_html}
        </div>

        <!-- Swiss Day Containers -->
        {swiss_containers_html}

        <!-- Swiss Accordion Full Briefing -->
        <div class="rounded-2xl bg-surface-container-lowest p-4 shadow-sm border border-border-subtle/40 space-y-2.5">
          <h4 class="font-bold text-primary text-[14px] flex items-center gap-1.5">
            <span class="material-symbols-outlined text-secondary text-[17px]">format_list_bulleted</span>
            <span>스위스 5박 6일 전 일정 브리핑 펼쳐보기</span>
          </h4>
          <div class="space-y-1.5">
            {swiss_accordion_html}
          </div>
        </div>

      </section>

    </main>

    <!-- ============================================================ -->
    <!-- FIXED BOTTOM NAVIGATION BAR                                  -->
    <!-- ============================================================ -->
    <nav class="fixed bottom-0 left-0 right-0 z-40 bg-canvas-ivory/95 backdrop-blur-md border-t border-border-subtle/60 px-4 py-2 pb-safe shadow-lg">
      <div class="grid grid-cols-4 gap-1 text-center">
        
        <button type="button" id="nav-btn-home" onclick="switchMainTab('home')" class="nav-btn py-1 flex flex-col items-center justify-center text-primary transition-colors">
          <span class="material-symbols-outlined text-[20px]">dashboard</span>
          <span class="text-[11px] font-bold tracking-tight mt-0.5">전체 개요</span>
        </button>

        <button type="button" id="nav-btn-uk" onclick="switchMainTab('uk')" class="nav-btn py-1 flex flex-col items-center justify-center text-on-surface-variant transition-colors">
          <span class="material-symbols-outlined text-[20px]">domain</span>
          <span class="text-[11px] tracking-tight mt-0.5">🇬🇧 런던</span>
        </button>

        <button type="button" id="nav-btn-paris" onclick="switchMainTab('paris')" class="nav-btn py-1 flex flex-col items-center justify-center text-on-surface-variant transition-colors">
          <span class="material-symbols-outlined text-[20px]">palette</span>
          <span class="text-[11px] tracking-tight mt-0.5">🇫🇷 파리</span>
        </button>

        <button type="button" id="nav-btn-swiss" onclick="switchMainTab('swiss')" class="nav-btn py-1 flex flex-col items-center justify-center text-on-surface-variant transition-colors">
          <span class="material-symbols-outlined text-[20px]">landscape</span>
          <span class="text-[11px] tracking-tight mt-0.5">🇨🇭 스위스</span>
        </button>

      </div>
    </nav>

    <!-- ============================================================ -->
    <!-- VOUCHER QUICK MODAL                                          -->
    <!-- ============================================================ -->
    <div id="voucherModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 hidden">
      <div class="w-full max-w-sm rounded-2xl bg-surface-container-lowest shadow-2xl border border-border-subtle/50 overflow-hidden flex flex-col max-h-[85dvh]">
        
        <div class="px-4 py-3 bg-surface-cream border-b border-border-subtle/50 flex items-center justify-between shrink-0">
          <div class="flex items-center gap-1.5">
            <span class="material-symbols-outlined text-primary text-[18px]">bookmark</span>
            <h3 class="font-bold text-primary text-[15px]">확정 바우처 모아보기</h3>
          </div>
          <button type="button" onclick="closeVouchersModal()" class="w-7 h-7 rounded-full bg-surface-container text-on-surface flex items-center justify-center hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined text-[17px]">close</span>
          </button>
        </div>

        <div class="p-4 overflow-y-auto space-y-4 text-[13px]">
          
          <!-- 🇬🇧 런던 -->
          <div class="space-y-1.5">
            <h4 class="font-bold text-london-crimson text-[12.5px] uppercase tracking-wider">🇬🇧 영국 런던 & 옥스퍼드 (UK)</h4>
            <div class="space-y-1">
              <a href="https://www.klook.com/ko/experiences/booking_detail/?guid=5583938439&bookingNo=JNR875059&sub_category_id=171" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">train</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">히드로 익스프레스 직통 (JNR875059)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">클룩 ↗</span>
              </a>

              <a href="https://www.myrealtrip.com/reservations/EXP-20260809-00014349" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">photo_camera</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">런던 허니문 스냅 (08:30 빅벤 4번출구)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">예약 ↗</span>
              </a>

              <a href="https://www.klook.com/ko/experiences/booking_detail/?guid=5583382053&bookingNo=QKZ212209&sub_category_id=1" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">attractions</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">런던아이 패스트트랙 (10:30 확정 · QKZ212209)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">클룩예약 ↗</span>
              </a>

              <a href="https://www.klook.com/ko/experiences/booking_detail/?guid=5583448316&bookingNo=EYY349639&sub_category_id=1" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">church</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">세인트폴 대성당 돔 (13:30 확정 · EYY349639)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">클룩예약 ↗</span>
              </a>

              <a href="https://www.airbnb.co.kr/trips/v1/1677481706963156774" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">home</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">소호 에어비앤비 5박 (Dean St)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">에어비앤비 ↗</span>
              </a>

              <!-- 옥스퍼드 3종 신설 추가 -->
              <a href="https://kr.trip.com/trains/uk/" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">train</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">옥스퍼드 왕복 기차표 (09:38 발)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">트립닷컴 ↗</span>
              </a>

              <a href="./vouchers/christ_church_ticket.png" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">qr_code_2</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">옥스퍼드 크라이스트 처치 (QR 티켓 확정)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">QR 티켓 ↗</span>
              </a>

              <a href="https://www.oxfordpunting.co.uk/prices/" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">kayaking</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">모들린 브리지 사공 펀팅 (11:00)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">펀팅공식 ↗</span>
              </a>

              <a href="https://www.klook.com/ko/ptp/order-details/?order_no=5432599190" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">train</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">유로스타 9032 (9/15 13:31 · 주문 5432599190)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">클룩주문 ↗</span>
              </a>

              <a href="https://www.gov.uk/guidance/apply-for-an-electronic-travel-authorisation-eta" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-london-crimson text-[18px] shrink-0">badge</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">영국 ETA 전자여행허가 (완료)</span>
                </div>
                <span class="text-[11px] text-london-crimson font-medium shrink-0">영국정부 ↗</span>
              </a>
            </div>
          </div>

          <!-- 🇫🇷 파리 -->
          <div class="space-y-1.5">
            <h4 class="font-bold text-parisian-rose text-[12.5px] uppercase tracking-wider">🇫🇷 프랑스 파리 (Paris)</h4>
            <div class="space-y-1">
              <a href="https://www.klook.com/ko/voucher-new/8c58a9bc-5acc-41ad-4040-7ba6a90ebbf4?lang=ko_KR&spm=BookingDetail.ViewVoucher&clickId=0efbcca78b" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-parisian-rose text-[18px] shrink-0">museum</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">루브르 박물관 (9/16 14:30 확정)</span>
                </div>
                <span class="text-[11px] text-parisian-rose font-medium shrink-0">바우처 ↗</span>
              </a>

              <a href="https://www.klook.com/ko/experiences/booking_detail/?guid=5583092533&bookingNo=ZKN582328&sub_category_id=1" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-parisian-rose text-[18px] shrink-0">castle</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">베르사유 궁전 예약상세 (ZKN582328)</span>
                </div>
                <span class="text-[11px] text-parisian-rose font-medium shrink-0">클룩예약 ↗</span>
              </a>

              <a href="https://www.klook.com/klvoucher/REZJbmVJUXhSV2V6UjZCcDl2TXNDdkZHTjN5cVhaaVYrb05HdGpEdXRpbnNWTmwreDJVaU5XZ0VNelpEczNxemZvbU5lRVRPSnNXa0hla3dTUHh1cHFpcjk2K21yaXZmRllLY2czdlo0Z0k9.pdf?spm=BookingDetail.ViewVoucher&clickId=53426a21ce" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-parisian-rose text-[18px] shrink-0">picture_as_pdf</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">베르사유 궁전 바우처 PDF</span>
                </div>
                <span class="text-[11px] text-parisian-rose font-medium shrink-0">PDF ↗</span>
              </a>

              <a href="https://www.airbnb.co.kr/trips/v1/reservation-details/ro/RESERVATION2_CHECKIN/HMJNDQRQSC" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-parisian-rose text-[18px] shrink-0">home</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">파리 15구 숙소 3박 (에펠탑 인근)</span>
                </div>
                <span class="text-[11px] text-parisian-rose font-medium shrink-0">에어비앤비 ↗</span>
              </a>

              <a href="https://www.klook.com/ko/add-upcoming-trip/?id=2ac7ebb5-7712-4e8e-4fc6-5c8ad540c6ad&utm_campaign=platform-share&utm_content=platform%3Dapp_pagespm%3DShareBookingPreview_textversion%3D1_shareid%3Dcfdf8d05-e37c-40b9-b6b6-f68d6c0fb60f&utm_medium=kakao-talk&utm_source=kakao" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-parisian-rose text-[18px] shrink-0">train</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">TGV Lyria 9211 (9/18 10:22 확정예약)</span>
                </div>
                <span class="text-[11px] text-parisian-rose font-medium shrink-0">클룩예약 ↗</span>
              </a>
            </div>
          </div>

          <!-- 🇨🇭 스위스 -->
          <div class="space-y-1.5">
            <h4 class="font-bold text-secondary text-[12.5px] uppercase tracking-wider">🇨🇭 스위스 알프스 (Swiss)</h4>
            <div class="space-y-1">
              <a href="https://www.airbnb.co.kr/trips/v1/1681698459825419428" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-secondary text-[18px] shrink-0">home</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">인터라켄 운터젠 숙소 2박 (에어비앤비)</span>
                </div>
                <span class="text-[11px] text-secondary font-medium shrink-0">에어비앤비 ↗</span>
              </a>

              <a href="https://www.jungfrau.co.kr" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-secondary text-[18px] shrink-0">ramen_dining</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">동신항운 신라면 쿠폰 (종이 인쇄 완료)</span>
                </div>
                <span class="text-[11px] text-secondary font-medium shrink-0">동신항운 ↗</span>
              </a>

              <a href="./vouchers/sunstar_hotel.pdf" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-secondary text-[18px] shrink-0">picture_as_pdf</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">선스타 호텔 그린델발트 (아고다 PDF 바우처)</span>
                </div>
                <span class="text-[11px] text-secondary font-medium shrink-0">바우처 PDF ↗</span>
              </a>

              <a href="./vouchers/zurich_stay.pdf" target="_blank" rel="noopener noreferrer" class="p-2.5 rounded-xl bg-surface-cream hover:bg-surface-container flex items-center justify-between transition-colors">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-secondary text-[18px] shrink-0">picture_as_pdf</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">취리히 중앙역 MANY'S 숙소 (PDF 바우처)</span>
                </div>
                <span class="text-[11px] text-secondary font-medium shrink-0">바우처 PDF ↗</span>
              </a>

              <div class="p-2.5 rounded-xl bg-surface-cream flex items-center justify-between">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="material-symbols-outlined text-secondary text-[18px] shrink-0">confirmation_number</span>
                  <span class="font-semibold text-primary truncate text-[12.5px]">스위스 트래블 패스 4일권 (9/18~9/21 연속)</span>
                </div>
                <span class="text-[11px] text-secondary font-bold shrink-0">개시확정</span>
              </div>
            </div>
          </div>

        </div>

        <div class="p-3 bg-surface-cream border-t border-border-subtle/50 text-center shrink-0">
          <button type="button" onclick="closeVouchersModal()" class="w-full py-2 rounded-xl bg-primary text-white font-bold text-[13px] hover:bg-primary/90 transition-colors">
            닫기
          </button>
        </div>

      </div>
    </div>

    <!-- Emergency SOS Modal -->
    <div id="sosModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-end sm:items-center justify-center p-0 sm:p-4 hidden opacity-0 transition-opacity duration-200">
      <div class="bg-surface-container-lowest w-full max-w-[480px] max-h-[85vh] rounded-t-3xl sm:rounded-3xl shadow-xl flex flex-col overflow-hidden border border-border-subtle/50">
        
        <div class="p-4 border-b border-border-subtle/50 flex items-center justify-between bg-surface-cream shrink-0">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 rounded-full bg-london-crimson text-white flex items-center justify-center shadow-xs">
              <span class="material-symbols-outlined text-[18px]">emergency</span>
            </div>
            <div>
              <h3 class="font-bold text-primary text-[15px] font-serif">비상 SOS 원터치 연락망</h3>
              <p class="text-[11px] text-on-surface-variant">대사관 · 긴급전화 · 영사콜센터 · 카드분실</p>
            </div>
          </div>
          <button type="button" onclick="closeSosModal()" class="p-1.5 rounded-full hover:bg-surface-container text-on-surface-variant transition-colors">
            <span class="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        <div class="p-4 space-y-3.5 overflow-y-auto overscroll-contain flex-1 text-[13px]">
          <!-- 24시간 외교부 영사콜센터 -->
          <div class="p-3 rounded-xl bg-london-crimson/10 border border-london-crimson/20 space-y-1.5">
            <div class="flex items-center justify-between">
              <span class="font-bold text-london-crimson flex items-center gap-1.5">
                <span class="material-symbols-outlined text-[16px]">support_agent</span>
                외교부 영사콜센터 (24시간)
              </span>
              <a href="tel:+82232100404" class="px-2.5 py-1 rounded-lg bg-london-crimson text-white font-bold text-[11px] shadow-xs hover:bg-london-crimson/90">통화하기 📞</a>
            </div>
            <p class="text-[11.5px] text-on-surface-variant leading-snug">
              해외 사건사고 긴급 지원, 통역 지원: <a href="tel:+82232100404" class="font-bold text-primary underline">+82-2-3210-0404</a><br/>
              (카카오톡 플러스친구 '영사콜센터' 무료 상담 가능)
            </p>
          </div>

          <!-- 국가별 대사관 & 긴급전화 -->
          <div class="space-y-2">
            <h4 class="font-bold text-primary text-[12px] flex items-center gap-1">
              <span class="material-symbols-outlined text-[15px]">flag</span>
              국가별 대사관 & 현지 긴급신고
            </h4>

            <!-- 🇬🇧 영국 -->
            <div class="p-2.5 rounded-xl bg-surface-cream border border-border-subtle/40 space-y-1">
              <div class="flex items-center justify-between font-bold text-primary">
                <span>🇬🇧 영국 (런던)</span>
                <span class="text-[11px] text-london-crimson font-mono font-bold">긴급: 999</span>
              </div>
              <div class="flex items-center justify-between text-[11.5px] text-on-surface-variant">
                <span>주영국 대사관 긴급전화:</span>
                <a href="tel:+447876508082" class="font-bold text-primary underline">+44-7876-508-082</a>
              </div>
              <div class="flex items-center justify-between text-[11px] text-on-surface-variant/80">
                <span>대사관 대표전화:</span>
                <a href="tel:+442072275500" class="underline">+44-20-7227-5500</a>
              </div>
            </div>

            <!-- 🇫🇷 프랑스 -->
            <div class="p-2.5 rounded-xl bg-surface-cream border border-border-subtle/40 space-y-1">
              <div class="flex items-center justify-between font-bold text-primary">
                <span>🇫🇷 프랑스 (파리)</span>
                <span class="text-[11px] text-parisian-rose font-mono font-bold">긴급: 112 (경찰 17)</span>
              </div>
              <div class="flex items-center justify-between text-[11.5px] text-on-surface-variant">
                <span>주프랑스 대사관 긴급전화:</span>
                <a href="tel:+33680285396" class="font-bold text-primary underline">+33-6-8028-5396</a>
              </div>
              <div class="flex items-center justify-between text-[11px] text-on-surface-variant/80">
                <span>대사관 대표전화:</span>
                <a href="tel:+33147530101" class="underline">+33-1-4753-0101</a>
              </div>
            </div>

            <!-- 🇨🇭 스위스 -->
            <div class="p-2.5 rounded-xl bg-surface-cream border border-border-subtle/40 space-y-1">
              <div class="flex items-center justify-between font-bold text-primary">
                <span>🇨🇭 스위스 (베른/취리히)</span>
                <span class="text-[11px] text-secondary font-mono font-bold">긴급: 112 (경찰 117)</span>
              </div>
              <div class="flex items-center justify-between text-[11.5px] text-on-surface-variant">
                <span>주스위스 대사관 긴급전화:</span>
                <a href="tel:+41798974086" class="font-bold text-primary underline">+41-79-897-4086</a>
              </div>
              <div class="flex items-center justify-between text-[11px] text-on-surface-variant/80">
                <span>대사관 대표전화:</span>
                <a href="tel:+41313562444" class="underline">+41-31-356-2444</a>
              </div>
            </div>
          </div>

          <!-- 카드 분실 & 로밍센터 -->
          <div class="space-y-1.5 pt-1">
            <h4 class="font-bold text-primary text-[12px] flex items-center gap-1">
              <span class="material-symbols-outlined text-[15px]">credit_card</span>
              카드 분실신고 & 통신사 로밍 고객센터
            </h4>
            <div class="grid grid-cols-2 gap-2 text-[11px]">
              <div class="p-2 rounded-lg bg-surface-cream border border-border-subtle/40">
                <span class="font-bold text-primary block">트래블월렛 분실신고</span>
                <a href="tel:+8215228220" class="text-primary font-mono underline">+82-1522-8220</a>
              </div>
              <div class="p-2 rounded-lg bg-surface-cream border border-border-subtle/40">
                <span class="font-bold text-primary block">하나카드 (트래블로그)</span>
                <a href="tel:+8218001111" class="text-primary font-mono underline">+82-1800-1111</a>
              </div>
              <div class="p-2 rounded-lg bg-surface-cream border border-border-subtle/40">
                <span class="font-bold text-primary block">SKT 로밍 (무료)</span>
                <a href="tel:+82263439000" class="text-primary font-mono underline">+82-2-6343-9000</a>
              </div>
              <div class="p-2 rounded-lg bg-surface-cream border border-border-subtle/40">
                <span class="font-bold text-primary block">KT 로밍 (무료)</span>
                <a href="tel:+82221900901" class="text-primary font-mono underline">+82-2-2190-0901</a>
              </div>
            </div>
          </div>

        </div>

        <div class="p-3 bg-surface-cream border-t border-border-subtle/50 text-center shrink-0">
          <button type="button" onclick="closeSosModal()" class="w-full py-2 rounded-xl bg-primary text-white font-bold text-[13px] hover:bg-primary/90 transition-colors">
            닫기
          </button>
        </div>

      </div>
    </div>

  </div> <!-- /#app-shell -->

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <!-- Client-side Logic -->
  <script>
    const PINS = {json.dumps(PINS, ensure_ascii=False)};
    const DAY_MAP_CONFIG = {json.dumps(DAY_MAP_CONFIG, ensure_ascii=False)};

    // Leaflet active map instance
    let activeMap = null;
    let activeMapKey = null;

    // SafeStorage Service (with pre-flight verification & memory fallback)
    const SafeStorage = (() => {{
      let backend = null;
      const mem = {{
        _d: {{}},
        getItem(k) {{ return Object.prototype.hasOwnProperty.call(this._d, k) ? this._d[k] : null; }},
        setItem(k, v) {{ this._d[k] = String(v); }},
        removeItem(k) {{ delete this._d[k]; }}
      }};

      try {{
        const testKey = "__hm_test__";
        window.localStorage.setItem(testKey, "1");
        window.localStorage.removeItem(testKey);
        backend = window.localStorage;
      }} catch (e) {{
        console.warn("[SafeStorage] localStorage unavailable. Fallback to memory.", e);
        backend = mem;
      }}

      return {{
        get(k) {{
          try {{ return backend.getItem(k); }}
          catch (e) {{ return mem.getItem(k); }}
        }},
        set(k, v) {{
          try {{ backend.setItem(k, String(v)); }}
          catch (e) {{ backend = mem; mem.setItem(k, String(v)); }}
        }}
      }};
    }})();

    // App State Manager
    const AppStore = {{
      defaults: {{
        uk: "uk-d0",
        paris: "paris-d1",
        swiss: "swiss-d8"
      }},
      getActiveTab() {{
        return SafeStorage.get("hm_active_tab") || "home";
      }},
      setActiveTab(t) {{
        SafeStorage.set("hm_active_tab", t);
      }},
      getActiveDay(cKey) {{
        return SafeStorage.get("hm_day_" + cKey) || this.defaults[cKey] || (cKey + "-d0");
      }},
      setActiveDay(cKey, dKey) {{
        SafeStorage.set("hm_day_" + cKey, dKey);
      }}
    }};

    // D-Day Calculator (KST midnight-based calendar difference)
    function updateDDay() {{
      const now = new Date();
      const utcNow = now.getTime() + (now.getTimezoneOffset() * 60 * 1000);
      const kstNow = new Date(utcNow + (9 * 60 * 60 * 1000));
      
      const todayKst = new Date(kstNow.getFullYear(), kstNow.getMonth(), kstNow.getDate());
      const targetKst = new Date(2026, 8, 10); // 2026-09-10 (month index 8)

      const diffMs = targetKst - todayKst;
      const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

      const badge = document.getElementById("dday-badge");
      if (badge) {{
        if (diffDays > 0) {{
          badge.textContent = "D-" + diffDays;
        }} else if (diffDays === 0) {{
          badge.textContent = "D-DAY 오늘 출국! ✈️";
        }} else if (diffDays >= -13) {{
          badge.textContent = "여행 " + (Math.abs(diffDays) + 1) + "일차 ❤️";
        }} else {{
          badge.textContent = "D+" + Math.abs(diffDays);
        }}
      }}
    }}

    // Switch Main Screens (Overview, UK, Paris, Swiss)
    function switchMainTab(tabKey, restoreDay = true, smoothScroll = false) {{
      cleanupActiveMap();
      const screens = document.querySelectorAll(".screen-page");
      screens.forEach(s => {{
        const isActive = (s.id === "screen-" + tabKey);
        s.classList.toggle("hidden", !isActive);
      }});

      // Update Nav Buttons
      ["home", "uk", "paris", "swiss"].forEach(id => {{
        const btn = document.getElementById("nav-btn-" + id);
        if (!btn) return;
        const isTarget = (id === tabKey);
        btn.classList.toggle("text-primary", isTarget);
        btn.classList.toggle("text-on-surface-variant", !isTarget);
        const span = btn.querySelector("span:last-child");
        if (span) span.classList.toggle("font-bold", isTarget);
      }});

      AppStore.setActiveTab(tabKey);

      if (smoothScroll) {{
        window.scrollTo({{ top: 0, behavior: "smooth" }});
      }}

      // Restore active day for country screens
      if (restoreDay && tabKey !== "home") {{
        const targetDay = AppStore.getActiveDay(tabKey);
        selectDayChip(tabKey, targetDay, false);
      }}
    }}

    // Select Day Chip
    function selectDayChip(cKey, dKey, switchTabIfNeeded = true) {{
      if (switchTabIfNeeded) {{
        const currentScreen = document.getElementById("screen-" + cKey);
        if (!currentScreen || currentScreen.classList.contains("hidden")) {{
          switchMainTab(cKey, false, false);
        }}
      }}

      if (activeMap && activeMapKey !== dKey) {{
        cleanupActiveMap();
      }}

      // Toggle day containers
      const containers = document.querySelectorAll("#screen-" + cKey + " .country-day-container");
      containers.forEach(el => el.classList.add("hidden"));

      let target = document.getElementById("container-" + cKey + "-" + dKey);
      if (!target) {{
        dKey = AppStore.defaults[cKey];
        target = document.getElementById("container-" + cKey + "-" + dKey);
      }}
      if (target) target.classList.remove("hidden");

      // Update chip styles
      const scroller = document.getElementById("scroller-" + cKey);
      if (scroller) {{
        const chips = scroller.querySelectorAll(".day-chip");
        chips.forEach(btn => {{
          const isTarget = (btn.id === "chip-" + cKey + "-" + dKey);
          btn.classList.toggle("bg-primary-container", isTarget);
          btn.classList.toggle("text-on-primary", isTarget);
          btn.classList.toggle("shadow-sm", isTarget);
          btn.classList.toggle("ring-1", isTarget);
          btn.classList.toggle("ring-london-crimson/20", isTarget);
          btn.classList.toggle("bg-surface-container-lowest", !isTarget);
          btn.classList.toggle("text-on-surface", !isTarget);

          const topSpan = btn.querySelector("span:first-child");
          if (topSpan) {{
            topSpan.classList.toggle("text-parisian-rose", isTarget);
            topSpan.classList.toggle("font-bold", isTarget);
            topSpan.classList.toggle("text-on-surface-variant", !isTarget);
          }}

          if (isTarget) {{
            btn.scrollIntoView({{ behavior: "smooth", inline: "center", block: "nearest" }});
          }}
        }});
      }}

      AppStore.setActiveDay(cKey, dKey);

      // Invalidate map if active
      if (activeMap && activeMapKey === dKey) {{
        requestAnimationFrame(() => {{
          activeMap.invalidateSize();
          if (activeMap._fitBounds) activeMap.fitBounds(activeMap._fitBounds, {{ padding: [20, 20] }});
        }});
      }}
    }}

    // Jump to specific day from calendar or external buttons
    function jumpToDay(cKey, dKey) {{
      switchMainTab(cKey, false, true);
      selectDayChip(cKey, dKey, false);
      
      // Update calendar button styling
      document.querySelectorAll(".cal-day-btn").forEach(btn => {{
        const onclickStr = btn.getAttribute("onclick") || "";
        const isMatch = onclickStr.includes("'" + dKey + "'");
        btn.classList.toggle("ring-2", isMatch);
        btn.classList.toggle("ring-primary", isMatch);
      }});
    }}

    // Safely dispose active Leaflet instance to avoid memory leak
    function cleanupActiveMap() {{
      if (activeMap) {{
        if (activeMapKey) {{
          const prevWrap = document.getElementById("map-wrap-" + activeMapKey);
          const prevBtn = document.getElementById("btn-map-text-" + activeMapKey);
          if (prevWrap) prevWrap.classList.add("hidden");
          if (prevBtn) prevBtn.textContent = "지도 펼치기";
        }}
        try {{
          activeMap.remove();
        }} catch (e) {{
          console.warn("Leaflet map removal:", e);
        }}
        activeMap = null;
        activeMapKey = null;
      }}
    }}

    // Toggle Collapsible Day Leaflet Map (Safe memory disposal & double rAF)
    function toggleDayMap(dayKey) {{
      const wrap = document.getElementById("map-wrap-" + dayKey);
      const btnText = document.getElementById("btn-map-text-" + dayKey);
      if (!wrap) return;

      const isHidden = wrap.classList.contains("hidden");
      if (isHidden) {{
        cleanupActiveMap();

        wrap.classList.remove("hidden");
        if (btnText) btnText.textContent = "지도 접기";

        // Double requestAnimationFrame ensures browser reflow before Leaflet measures dimensions
        requestAnimationFrame(() => {{
          requestAnimationFrame(() => {{
            initDayMap(dayKey);
          }});
        }});
      }} else {{
        cleanupActiveMap();
      }}
    }}

    // Initialize Leaflet Map
    function initDayMap(dayKey) {{
      if (typeof L === "undefined") return;
      const mapDiv = document.getElementById("map-" + dayKey);
      if (!mapDiv) return;

      if (activeMap && activeMapKey === dayKey) {{
        activeMap.invalidateSize();
        if (activeMap._fitBounds) activeMap.fitBounds(activeMap._fitBounds, {{ padding: [20, 20] }});
        return;
      }}

      const cfg = DAY_MAP_CONFIG[dayKey];
      if (!cfg || !cfg.mapKeys || cfg.mapKeys.length === 0) return;

      const startPin = PINS[cfg.defaultStartKey] || PINS[cfg.mapKeys[0]];
      const center = startPin ? startPin.ll : [51.505, -0.09];

      try {{
        const m = L.map(mapDiv, {{ scrollWheelZoom: false }}).setView(center, 13);
        L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
          maxZoom: 19, attribution: "© OpenStreetMap"
        }}).addTo(m);

        const markers = [];
        cfg.mapKeys.forEach(k => {{
          const p = PINS[k];
          if (!p) return;
          const gLink = (p && p.gUrl) ? p.gUrl : ("https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(p.name));
          const popup = `
            <div style="font-size:12.5px; font-family:sans-serif; line-height:1.4;">
              <b style="color:#1B2A4A;">${{p.name}}</b><br/>
              <span style="color:#6b6f76; font-size:11px;">Day ${{p.day}}</span><br/>
              <a href="${{gLink}}" target="_blank" rel="noopener noreferrer" style="display:inline-block; margin-top:5px; padding:3px 8px; background:#8B2635; color:#fff; border-radius:4px; font-size:11px; text-decoration:none; font-weight:bold;">
                🗺 구글맵 길찾기
              </a>
            </div>
          `;
          const mk = L.marker(p.ll).addTo(m).bindPopup(popup);
          markers.push(mk);
        }});

        if (markers.length >= 1) {{
          const fg = L.featureGroup(markers);
          const bounds = fg.getBounds();
          m._fitBounds = bounds;
          m.fitBounds(bounds, {{ padding: [20, 20], maxZoom: 15 }});
        }}

        activeMap = m;
        activeMapKey = dayKey;
      }} catch(e) {{
        console.warn("Leaflet map init failed on " + dayKey, e);
      }}
    }}

    // Legacy Checklist Migration Map
    const CHECK_LEGACY_MAP = {{
      "chk_uk_hex": ["chk_hex", "chk-all-hex"],
      "chk_uk_snap": ["chk_snap", "chk-all-snap"],
      "chk_uk_eye": ["chk_eye", "chk-all-eye"],
      "chk_uk_stpaul": ["chk_stpaul", "chk-all-stpaul"],
      "chk_ox_christ": ["chk-all-ox-christ"],
      "chk_eurostar": ["chk_uk_eurostar", "chk-all-eurostar"],
      "chk_fr_louvre": ["chk_louvre", "chk-all-louvre"],
      "chk_fr_versailles": ["chk_versailles", "chk-all-versailles"],
      "chk_tgv_lyria": ["chk_tgv", "chk-all-tgv"],
      "chk_sw_dongshin": ["chk_dongshin", "chk-all-dongshin"],
      "chk_sw_pass": ["chk_swisspass", "chk-all-swisspass"]
    }};

    // Initialize Checkboxes & Persistence (with Live Cross-Screen DOM Sync)
    function initCheckboxes() {{
      document.querySelectorAll("input[type=checkbox]").forEach(cb => {{
        const key = "chk_" + (cb.dataset.key || cb.id.replace(/^chk-all-/, ""));
        let saved = SafeStorage.get(key);

        // Fallback to legacy key if needed
        if (saved === null && CHECK_LEGACY_MAP[key]) {{
          for (const oldKey of CHECK_LEGACY_MAP[key]) {{
            const legacyVal = SafeStorage.get(oldKey);
            if (legacyVal !== null) {{
              saved = legacyVal;
              SafeStorage.set(key, legacyVal);
              break;
            }}
          }}
        }}

        if (saved !== null) {{
          cb.checked = (saved === "1");
        }}

        if (cb.parentElement) {{
          cb.parentElement.classList.toggle("opacity-60", cb.checked);
        }}

        cb.addEventListener("change", () => {{
          const isChecked = cb.checked;
          SafeStorage.set(key, isChecked ? "1" : "0");
          if (cb.parentElement) {{
            cb.parentElement.classList.toggle("opacity-60", isChecked);
          }}

          // Live cross-sync all matching checkboxes across screens
          const rawKey = cb.dataset.key || cb.id.replace(/^chk-all-/, "");
          document.querySelectorAll("input[type=checkbox]").forEach(other => {{
            if (other === cb) return;
            const otherRawKey = other.dataset.key || other.id.replace(/^chk-all-/, "");
            if (otherRawKey === rawKey || "chk_" + otherRawKey === key) {{
              other.checked = isChecked;
              if (other.parentElement) {{
                other.parentElement.classList.toggle("opacity-60", isChecked);
              }}
            }}
          }});
        }});
      }});
    }}

    // Vouchers Modal Controls (with Body Scroll Lock)
    function openVouchersModal() {{
      const modal = document.getElementById("voucherModal");
      if (modal) {{
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        document.body.style.overflow = "hidden";
      }}
    }}

    function closeVouchersModal() {{
      const modal = document.getElementById("voucherModal");
      if (modal) {{
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.style.overflow = "";
      }}
    }}

    // Emergency SOS Modal Controls
    function openSosModal() {{
      const modal = document.getElementById("sosModal");
      if (modal) {{
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        requestAnimationFrame(() => {{
          modal.classList.remove("opacity-0");
          modal.classList.add("opacity-100");
        }});
        document.body.style.overflow = "hidden";
      }}
    }}

    function closeSosModal() {{
      const modal = document.getElementById("sosModal");
      if (modal) {{
        modal.classList.remove("opacity-100");
        modal.classList.add("opacity-0");
        setTimeout(() => {{
          modal.classList.add("hidden");
          modal.classList.remove("flex");
          document.body.style.overflow = "";
        }}, 200);
      }}
    }}

    // Web Share API with Clipboard Fallback
    function shareTrip() {{
      const shareData = {{
        title: "Grand Tour Honeymoon · 13박 14일 유럽 허니문",
        text: "영국 런던 ➔ 프랑스 파리 ➔ 스위스 알프스 신혼여행 일정표입니다 💍",
        url: window.location.href
      }};

      if (navigator.share && navigator.canShare && navigator.canShare(shareData)) {{
        navigator.share(shareData).catch(err => {{
          if (err.name !== "AbortError") copyClipboardFallback();
        }});
      }} else {{
        copyClipboardFallback();
      }}
    }}

    function copyClipboardFallback() {{
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(window.location.href).then(() => {{
          alert("신혼여행 일정표 링크가 클립보드에 복사되었습니다! 💌");
        }}).catch(() => {{
          prompt("일정표 주소를 복사해주세요:", window.location.href);
        }});
      }} else {{
        prompt("일정표 주소를 복사해주세요:", window.location.href);
      }}
    }}

    // Open-Meteo Weather Service
{weather_service_js}

    // App Initialization
    document.addEventListener("DOMContentLoaded", () => {{
      updateDDay();
      initCheckboxes();
      WeatherService.init();

      // Restore active tab
      const savedTab = AppStore.getActiveTab();
      switchMainTab(savedTab, true, false);

      // Close modals on backdrop click
      const voucherModal = document.getElementById("voucherModal");
      if (voucherModal) {{
        voucherModal.addEventListener("click", (e) => {{
          if (e.target === voucherModal) closeVouchersModal();
        }});
      }}

      const sosModal = document.getElementById("sosModal");
      if (sosModal) {{
        sosModal.addEventListener("click", (e) => {{
          if (e.target === sosModal) closeSosModal();
        }});
      }}

      // Offline PWA Service Worker Registration
      if ("serviceWorker" in navigator) {{
        navigator.serviceWorker.register("./sw.js").catch(err => {{
          console.log("Service Worker registration skipped:", err);
        }});
      }}
    }});
  </script>
</body>
</html>
'''

# Write to index.html and honeymoon-trip.html
output_paths = [
    "/Users/kakao/sideproject/web/honey-moon/honeymoon-trip-plan/index.html",
    "/Users/kakao/sideproject/web/honey-moon/honeymoon-trip-plan/honeymoon-trip.html"
]

for p in output_paths:
    with open(p, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"SUCCESS: Written {len(full_html)} bytes to {p}")

print("All master files assembled!")
