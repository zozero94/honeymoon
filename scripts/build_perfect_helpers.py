# -*- coding: utf-8 -*-
"""
build_perfect_html.py
Assembles index.html and honeymoon-trip.html with all fixes and data intact.
"""

import os
import sys

# Import definitions
from generate_perfect_data import PINS, DAY_MAP_CONFIG, DAYS

def render_timeline_item(it):
    hl = it.get("highlight", False)
    hl_cls = "ring-1 ring-london-crimson/30 shadow-sm" if hl else "border border-border-subtle/40"
    
    # Place map link
    p = it.get("place")
    p_html = ""
    if p:
        p_title = p.get("title", "지도 보기")
        p_html = f'''
          <a href="{p['url']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-surface-cream text-primary hover:bg-surface-container font-label-caps text-[11px] font-semibold border border-border-subtle/60 transition-colors">
            <span class="material-symbols-outlined text-[13px] text-london-crimson">location_on</span>
            <span>{p_title} 지도 ↗</span>
          </a>
        '''

    # Voucher link
    v = it.get("voucher")
    v_html = ""
    if v:
        v_html = f'''
          <a href="{v['url']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-surface-cream text-london-crimson hover:bg-surface-container font-label-caps text-[11px] font-bold border border-london-crimson/20 transition-colors">
            <span>{v['title']}</span>
            <span class="material-symbols-outlined text-[12px]">open_in_new</span>
          </a>
        '''

    actions_html = ""
    if p_html or v_html:
        actions_html = f'''
        <div class="pt-1.5 flex flex-wrap items-center gap-1.5">
          {p_html}
          {v_html}
        </div>
        '''

    title_text = it['title']
    if p:
        title_html = f'''<h4 class="font-title-md text-primary font-semibold text-[14px] leading-snug"><a href="{p['url']}" target="_blank" rel="noopener noreferrer" class="hover:text-london-crimson hover:underline transition-colors">{title_text}</a></h4>'''
    else:
        title_html = f'''<h4 class="font-title-md text-primary font-semibold text-[14px] leading-snug">{title_text}</h4>'''

    return f'''
    <div class="w-full rounded-xl bg-surface-container-lowest p-space-md shadow-sm {hl_cls}">
      <div class="flex items-start gap-3">
        <div class="flex flex-col items-center shrink-0 w-12 text-center pt-0.5">
          <span class="font-label-md text-primary font-bold text-[13px]">{it['time']}</span>
          <div class="w-8 h-8 rounded-full bg-surface-container text-on-surface flex items-center justify-center mt-1.5">
            <span class="material-symbols-outlined text-[17px]">{it['icon']}</span>
          </div>
        </div>
        <div class="min-w-0 flex-1 space-y-1">
          <span class="px-2 py-0.5 rounded-full bg-surface-cream text-on-surface-variant font-label-caps text-[10px] font-bold">{it['badge']}</span>
          {title_html}
          <p class="font-body-sm text-on-surface-variant text-[12.5px] leading-relaxed">{it['desc']}</p>
          {actions_html}
        </div>
      </div>
    </div>
    '''

def render_check_item(ck):
    link_html = ""
    if ck.get("link"):
        link_html = f'''<a href="{ck['link']}" target="_blank" rel="noopener noreferrer" class="text-london-crimson font-bold text-xs underline ml-1">{ck.get('linkText', '링크')} ↗</a>'''
    checked_attr = "checked" if ck.get("checked") else ""
    return f'''
    <label class="flex items-center gap-2 text-[12.5px] text-on-surface cursor-pointer py-1 select-none">
      <input type="checkbox" data-key="{ck['key']}" {checked_attr} class="rounded border-border-subtle text-primary focus:ring-primary h-4 w-4">
      <span>{ck['label']}</span>
      {link_html}
    </label>
    '''

def render_day_container(dKey, d, is_default_visible=False):
    cKey = d["cKey"]
    hidden_cls = "" if is_default_visible else "hidden"
    
    tl_html = "\n".join([render_timeline_item(it) for it in d["timeline"]])
    ck_html = "\n".join([render_check_item(ck) for ck in d["checks"]])
    
    bridge_html = ""
    if d.get("bridgeBanner"):
        bb = d["bridgeBanner"]
        bridge_html = f'''
        <div class="p-2.5 rounded-xl bg-london-crimson/10 border border-london-crimson/25 flex items-center justify-between shadow-xs">
          <div class="flex items-center gap-1.5 min-w-0">
            <span class="material-symbols-outlined text-london-crimson text-[17px] shrink-0">connecting_airports</span>
            <span class="text-[12px] text-london-crimson font-bold truncate">{bb['text']}</span>
          </div>
          <button type="button" onclick="selectDayChip('{bb['cKey']}', '{bb['dKey']}')" class="px-2.5 py-1 rounded-md bg-london-crimson text-white text-[11px] font-bold shrink-0 hover:bg-london-crimson/90">
            일정 보기 ↗
          </button>
        </div>
        '''

    return f'''
    <div id="container-{cKey}-{dKey}" class="country-day-container space-y-space-md {hidden_cls}">
      {bridge_html}

      <!-- Day Header -->
      <div class="rounded-xl bg-surface-container-lowest p-space-md shadow-sm border border-border-subtle/40 space-y-2">
        <div class="flex items-center justify-between">
          <span class="px-2 py-0.5 rounded-full bg-primary-container text-on-primary font-label-caps text-[11px] font-bold">{d['dayNum']} · {d['date']}</span>
          <span id="weather-badge-{dKey}" onclick="WeatherService.toggleBadge('{dKey}')" class="weather-badge text-[11.5px] text-on-surface-variant flex items-center gap-1 cursor-pointer select-none hover:text-primary transition-colors py-0.5 px-1.5 rounded-md hover:bg-surface-container/60" data-day="{dKey}" title="탭하여 실시간 기온 ⇋ 예보 전환">
            <span id="weather-icon-{dKey}" class="material-symbols-outlined text-[14px] text-amber-500">wb_sunny</span>
            <span id="weather-text-{dKey}">{d['weather'].split('·')[0].strip()}</span>
          </span>
        </div>
        <h3 class="font-title-lg text-primary font-bold text-[16px] leading-snug">{d['title']}</h3>
        <p class="font-body-sm text-on-surface-variant text-[12.5px] leading-relaxed">{d['desc']}</p>
        
        <!-- Tip box -->
        <div class="p-2.5 rounded-lg bg-surface-cream border border-border-subtle/50 text-[12px] text-on-surface-variant leading-relaxed">
          <span class="font-bold text-primary">💡 현지 실전 팁: </span>{d['tip']}
        </div>

        <!-- Action Row -->
        <div class="flex items-center gap-2 pt-1">
          <a href="{d['googleMap']}" target="_blank" rel="noopener noreferrer" class="flex-1 py-2 rounded-lg bg-primary text-white font-semibold text-[12px] flex items-center justify-center gap-1.5 shadow-sm hover:bg-primary/90 transition-colors">
            <span class="material-symbols-outlined text-[15px]">directions</span>
            <span>🗺 구글맵 당일 동선</span>
          </a>
          <button type="button" onclick="toggleDayMap('{dKey}')" class="px-3.5 py-2 rounded-lg bg-surface-container text-on-surface font-semibold text-[12px] flex items-center gap-1.5 border border-border-subtle/50 hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined text-[15px]">map</span>
            <span id="btn-map-text-{dKey}">지도 펼치기</span>
          </button>
        </div>
      </div>

      <!-- Collapsible Map -->
      <div id="map-wrap-{dKey}" class="rounded-xl overflow-hidden shadow-sm border border-border-subtle/40 bg-surface-container-lowest hidden">
        <div class="px-3 py-1.5 bg-surface-container border-b border-border-subtle/40 flex items-center justify-between text-[11px] text-on-surface-variant">
          <span class="font-bold flex items-center gap-1">
            <span class="material-symbols-outlined text-[13px] text-primary">pin_drop</span>
            당일 주요 핀 & 동선
          </span>
          <span>핀 클릭 시 구글맵 길찾기</span>
        </div>
        <div id="map-{dKey}" style="height: 240px; width: 100%;"></div>
      </div>

      <!-- Timeline -->
      <div class="space-y-2">
        <div class="flex items-center justify-between px-1">
          <h4 class="font-title-md text-primary font-bold text-[14px]">시간대별 상세 타임라인</h4>
          <span class="text-[11px] text-on-surface-variant">{len(d['timeline'])}개 코스</span>
        </div>
        <div class="space-y-2">
          {tl_html}
        </div>
      </div>

      <!-- Daily Checks -->
      <div class="rounded-xl bg-surface-container-lowest p-space-md shadow-sm border border-border-subtle/40 space-y-1.5">
        <h4 class="font-title-md text-primary font-bold text-[13.5px] flex items-center gap-1.5">
          <span class="material-symbols-outlined text-secondary text-[16px]">fact_check</span>
          이날 예약 & 준비물 점검
        </h4>
        <div class="space-y-0.5 divide-y divide-border-subtle/30">
          {ck_html}
        </div>
      </div>
    </div>
    '''

def render_country_chips(cKey, day_keys, active_dkey):
    chips = []
    for dk in day_keys:
        d = DAYS[dk]
        is_active = (dk == active_dkey)
        bg = "bg-primary-container text-on-primary shadow-sm ring-1 ring-london-crimson/20" if is_active else "bg-surface-container-lowest text-on-surface"
        top_span_color = "text-parisian-rose font-bold" if is_active else "text-on-surface-variant"
        
        chips.append(f'''
        <button type="button" id="chip-{cKey}-{dk}" onclick="selectDayChip('{cKey}', '{dk}')" class="day-chip shrink-0 px-3.5 py-2 rounded-xl text-center transition-all {bg}">
          <span class="block font-label-caps text-[10px] {top_span_color}">{d['chipLabel']}</span>
          <span class="block font-title-md text-[13px] font-bold mt-0.5">{d['chipDate']}</span>
        </button>
        ''')
    return "\n".join(chips)

def render_accordion_item(dKey, d):
    return f'''
    <details class="group rounded-xl bg-surface-container-lowest border border-border-subtle/40 shadow-xs overflow-hidden">
      <summary class="flex items-center justify-between p-3.5 cursor-pointer select-none hover:bg-surface-container/30 transition-colors">
        <div class="flex items-center gap-2.5 min-w-0">
          <span class="px-2 py-0.5 rounded-full bg-surface-cream text-primary font-bold text-[11px] shrink-0">{d['dayNum']}</span>
          <span class="font-semibold text-primary text-[13px] truncate">{d['chipDate']} · {d['title']}</span>
        </div>
        <span class="material-symbols-outlined text-on-surface-variant text-[18px] group-open:rotate-180 transition-transform">expand_more</span>
      </summary>
      <div class="p-3.5 pt-1 border-t border-border-subtle/30 text-[12.5px] space-y-2 text-on-surface-variant">
        <p class="leading-relaxed">{d['desc']}</p>
        <div class="flex items-center justify-between pt-1">
          <button type="button" onclick="selectDayChip('{d['cKey']}', '{dKey}')" class="text-london-crimson font-bold text-[11.5px] flex items-center gap-0.5">
            <span>상세 타임라인 보기</span>
            <span class="material-symbols-outlined text-[13px]">arrow_forward</span>
          </button>
          <a href="{d['googleMap']}" target="_blank" rel="noopener noreferrer" class="text-secondary font-bold text-[11.5px]">
            🗺 구글맵 동선 ↗
          </a>
        </div>
      </div>
    </details>
    '''

print("Building HTML components...")
