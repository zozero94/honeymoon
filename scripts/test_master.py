# -*- coding: utf-8 -*-
with open("/Users/kakao/sideproject/web/honey-moon/honeymoon-trip-plan/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Check Screens
for s in ["screen-home", "screen-uk", "screen-paris", "screen-swiss"]:
    assert f'id="{s}"' in html, f"Missing screen {s}"
print("✓ 4 Screens verified")

# 2. Check Heathrow Express
assert "JNR875059" in html, "Missing Heathrow Express booking JNR875059"
assert "히드로 익스프레스" in html, "Missing Heathrow Express text"
print("✓ Heathrow Express & booking JNR875059 verified")

# 3. Check London Snap
assert "EXP-20260809-00014349" in html, "Missing Snap booking EXP-20260809-00014349"
assert "빅벤" in html, "Missing meeting point"
print("✓ London Snap & booking EXP-20260809-00014349 verified")

# 4. Check London Eye & St Paul
assert "QKZ212209" in html and "5583382053" in html, "Missing London Eye"
assert "EYY349639" in html and "5583448316" in html, "Missing St Paul"
assert "1677481706963156774" in html, "Missing Soho Airbnb link"
print("✓ London Eye, St Paul & Soho Airbnb vouchers verified")

# 5. Check Louvre & Versailles
assert "8c58a9bc-5acc-41ad-4040-7ba6a90ebbf4" in html, "Missing Louvre voucher"
assert "REZJbmVJUXhSV" in html, "Missing Versailles PDF"
print("✓ Louvre (14:30) & Versailles (11:30 PDF) vouchers verified")

# 6. Check Eurostar & TGV
assert "13:31" in html and "유로스타" in html, "Missing Eurostar 13:31"
assert "10:22" in html and "TGV" in html, "Missing TGV 10:22"
print("✓ Eurostar & TGV verified")

# 7. Check Swiss Stays & Passes
assert "Obere Gasse" in html, "Missing Unterseen stay"
assert "Sunstar Hotel" in html, "Missing Sunstar hotel"
assert "sunstar_hotel.pdf" in html, "Missing Sunstar hotel voucher PDF"
assert "MANY" in html, "Missing Zurich MANY'S"
assert "jungfrau.co.kr" in html, "Missing Dongshin coupon"
assert "스위스 트래블 패스" in html, "Missing Swiss Travel Pass"
print("✓ Swiss 3 stays, Sunstar PDF, Dongshin coupon, Swiss Pass verified")

# 8. Check CSS & Safe Area
assert "pt-safe" in html and "pb-safe" in html, "Missing safe area classes"
assert "env(safe-area-inset-bottom" in html, "Missing env safe area in CSS"
assert "max-width: 480px" in html, "Missing max-width 480px"
assert "100dvh" in html, "Missing 100dvh"
print("✓ CSS Safe Area & 480px container verified")

# 9. Check Swiss Day 11 typo fix
assert "9/21 월" in html, "Missing 9/21 월"
assert "chip-swiss-swiss-d11" in html, "Missing swiss-d11 chip"
import re
swiss_chips = re.findall(r'id="chip-swiss-swiss-d11"[^>]*>(.*?)</button>', html, re.DOTALL)
assert len(swiss_chips) > 0
for sc in swiss_chips:
    assert "9/21 월" in sc, f"Typo still in swiss-d11: {sc}"
print("✓ Swiss Day 11 typo fixed to 9/21 월")

# 10. Check D-Day Midnight Logic
assert "targetKst" in html and "todayKst" in html, "Missing KST midnight logic in updateDDay"
print("✓ D-Day KST midnight logic verified")

# 11. Check Bilateral Bridge Banners
assert "오늘 오전 런던" in html, "Missing London bridge banner"
assert "오늘 오전 파리" in html, "Missing Paris bridge banner"
print("✓ Cross-border bridge banners verified")

# 12. Check Leaflet Memory Clean Up
assert "activeMap.remove()" in html, "Missing activeMap.remove() in toggleDayMap"
print("✓ Leaflet memory cleanup verified")

# 13. Check Identical files
with open("/Users/kakao/sideproject/web/honey-moon/honeymoon-trip-plan/honeymoon-trip.html", "r", encoding="utf-8") as f2:
    html2 = f2.read()
assert html == html2, "Files index.html and honeymoon-trip.html are NOT identical!"
print("✓ index.html and honeymoon-trip.html are 100% identical")

# 14. Check Confirmed UK Google Maps routes & spot links
assert "ado6i4GJfmmh6T5N8" in html, "Missing St James Lake short link"
assert "YmP2PP7WeX1B4Uca6" in html, "Missing Oxford punting short link"
assert "4ha3AWaDVGbiTyG58" in html, "Missing Christ Church short link"
assert "Lancaster+Road+London" in html, "Missing Lancaster road route"
assert "옥스퍼드+세인트+메리+대학교회" in html, "Missing St Mary church in Oxford route"
assert "옥스퍼드+탄식의+다리" in html, "Missing Bridge of Sighs in Oxford route"
assert "christ_church_ticket.png" in html, "Missing Christ Church QR ticket image"
print("✓ UK Google Maps confirmed routes & spots verified")
print("✓ Christ Church QR ticket verified")

# 15. Check Open-Meteo WeatherService Integration
assert "WeatherService" in html, "Missing WeatherService JS"
assert "weather-badge-uk-d0" in html, "Missing day weather badge"
assert "home-weather-uk" in html, "Missing overview weather widget"
assert "header-weather-uk" in html, "Missing header weather bar"
print("✓ Open-Meteo live weather service & widgets verified")

# 16. Check Confirmed Paris Google Maps routes & spot links
assert "viyUDpcB2fStvBdr9" in html, "Missing user Champ de Mars lawn short link"
assert "Gare+Champ+de+Mars+Tour+Eiffel" in html, "Missing Champ de Mars RER C station"
assert "Gare+de+Versailles+Château+Rive+Gauche" in html, "Missing Versailles Château station"
assert "Galerie+des+Glaces+Versailles" in html, "Missing Hall of Mirrors link"
assert "La+Petite+Venise+Versailles" in html, "Missing Petite Venise lunch link"
assert "Gare+de+Lyon+Hall+1+Paris" in html, "Missing TGV Gare de Lyon Hall 1 link"
assert "파리+노트르담+대성당" in html, "Missing Notre-Dame link"
assert "파리+셰익스피어+앤+컴퍼니" in html, "Missing Shakespeare link"
assert "파리+카페+드+플로르" in html, "Missing Cafe de Flore link"
assert "파리+루브르+박물관" in html, "Missing Louvre link"
assert "파리+튀일리+정원" in html, "Missing Tuileries link"
assert "베르사유+궁전" in html, "Missing Versailles Palace link"
assert "파리+보주+광장" in html, "Missing Place des Vosges link"
assert "Rue+des+Francs-Bourgeois+Paris" in html, "Missing Francs-Bourgeois link"
assert "Pont+Marie+Paris" in html, "Missing Pont Marie link"
assert "파리+리옹+역" in html, "Missing Gare de Lyon link"
print("✓ Paris Google Maps confirmed routes & spots verified (16 places)")

# 17. Check Confirmed Swiss Google Maps routes & spot links
assert "y6RKT6KzjU36vwKz5" in html, "Missing Unterseen stay user short link"
assert "gNWaSyYtJ3hHhdvN8" in html, "Missing Brienz lake user short link"
assert "jhqmm6j4KwWM49eM7" in html, "Missing Grindelwald Terminal user short link"
assert "B8SGZUuTvtzbXYB88" in html, "Missing Jungfrau user short link"
assert "MN3EfGgv1VzWBgmL8" in html, "Missing Interlaken Ost user short link"
assert "1c59w2UuBGuBFzs96" in html, "Missing Grindelwald station user short link"
assert "NYB4ym27aWDT9XUG7" in html, "Missing Lauterbrunnen Staubbach user short link"
assert "8pWWJtCLs7mzokFU8" in html, "Missing Bahnhofstrasse user short link"
assert "7ZVEYoLUxPrstAaJ9" in html, "Missing Incheon T2 user short link"
assert "Luftseilbahn+Pfingstegg" in html, "Missing Luftseilbahn Pfingstegg in Day 10 route"
assert "Beckenhofstrasse+7" in html, "Missing Beckenhofstrasse 7 in Day 11 route"
assert "취리히+공항" in html, "Missing Zurich Airport query"
assert "인천국제공항 제2여객터미널" in html, "Missing Incheon Airport T2 text"
print("✓ Switzerland Google Maps confirmed routes & spots verified (all days & custom short links)")

# 18. Check Emergency SOS Modal & Contacts
assert "openSosModal()" in html, "Missing openSosModal function or button call"
assert 'id="sosModal"' in html, "Missing #sosModal container"
assert "+82232100404" in html or "+82-2-3210-0404" in html, "Missing Consular Call Center"
assert "+442072275500" in html, "Missing UK embassy number"
assert "+33147530101" in html, "Missing France embassy number"
assert "+41313562444" in html or "+41798974086" in html, "Missing Swiss embassy number"
assert "카드 분실" in html, "Missing card loss section"
print("✓ Emergency SOS Modal & 1-tap dial contacts verified")

# 19. Check Christ Church in Master Checklist
assert "chk-all-ox-christ" in html, "Missing chk-all-ox-christ in master checklist"
print("✓ Christ Church checklist item verified")

# 20. Check Oxford Punting Time (11:00, not 15:30)
assert "모들린 브리지 사공 펀팅 (11:00)" in html, "Missing corrected Oxford Punting time (11:00)"
assert "15:30" not in html or "펀팅 (15:30)" not in html, "Found stale 15:30 Punting time"
print("✓ Oxford Punting time verified (11:00)")

# 21. Check Service Worker Registration
assert "serviceWorker" in html and "sw.js" in html, "Missing Service Worker registration"
print("✓ PWA Service Worker registration verified")

# 22. Check Flight details (KE907 & KE934)
assert "KE907" in html, "Missing Flight KE907"
assert "KE934" in html, "Missing Flight KE934"
print("✓ Flight numbers KE907 & KE934 verified")

# 23. Check Day 8 Bus 103 boarding location
assert "인터라켄 웨스트" in html and "103번 버스" in html, "Missing Interlaken West station for Bus 103"
print("✓ Day 8 Bus 103 boarding station verified")

# 24. Check Cleanup active map and live checkbox sync
assert "cleanupActiveMap" in html, "Missing cleanupActiveMap function"
assert "data-key" in html, "Missing data-key attribute for live checkbox sync"
print("✓ Leaflet cleanupActiveMap & live checkbox sync verified")

print("\n==========================================")
print("ALL 24 COMPREHENSIVE TESTS PASSED PERFECTLY!")
print("==========================================")
