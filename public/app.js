let currentFilter = 'all';
let currentView = 'rooms'; // 'rooms' or 'calendar'
let globalFloorsData = null;
let residentsMap = new Map();

// Admin Auth State
let adminToken = localStorage.getItem('dorm_admin_token') || '';
let isAdmin = !!adminToken;

// Calendar state: August 2026
let calYear = 2026;
let calMonth = 8;
let globalDutyCalendarData = null;

document.addEventListener('DOMContentLoaded', () => {
    updateAdminUI();
    fetchStats();
    fetchFloorsData();
    fetchTodayDuty();

    window.onLanguageChange = function() {
        updateAdminUI();
        if (window.i18n) window.i18n.applyTranslations();
        if (currentView === 'rooms') renderApp();
        if (currentView === 'calendar') fetchDutyCalendar();
        fetchTodayDuty();
    };


    // Attach click listeners to view mode buttons explicitly
    const btnRooms = document.getElementById('viewRoomsBtn');
    const btnCal = document.getElementById('viewCalendarBtn');

    if (btnRooms) {
        btnRooms.addEventListener('click', (e) => {
            e.preventDefault();
            switchView('rooms');
        });
    }

    if (btnCal) {
        btnCal.addEventListener('click', (e) => {
            e.preventDefault();
            switchView('calendar');
        });
    }

    // Modal listeners
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeResidentModal();
            closeDutyModal();
            closeLogsModal();
            closeAdminLoginModal();
        }
    });

    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                closeResidentModal();
                closeDutyModal();
                closeLogsModal();
                closeAdminLoginModal();
            }
        });
    });
});

function getAdminHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (adminToken) {
        headers['X-Admin-Token'] = adminToken;
    }
    return headers;
}

function updateAdminUI() {
    isAdmin = !!adminToken;
    
    // Toggle Admin Only buttons
    document.querySelectorAll('.admin-only-btn').forEach(btn => {
        btn.style.display = isAdmin ? 'inline-flex' : 'none';
    });

    // Admin Badge
    const badge = document.getElementById('adminBadge');
    if (badge) badge.style.display = isAdmin ? 'inline-flex' : 'none';

    // Auth Button text
    const authBtn = document.getElementById('adminAuthBtn');
    if (authBtn) {
        const icon = isAdmin ? 'fa-right-from-bracket' : 'fa-lock';
        const label = isAdmin ? window.i18n.t('btn_admin_logout') : window.i18n.t('btn_admin_login');
        authBtn.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${label}</span>`;
        authBtn.className = isAdmin ? "btn btn-danger" : "btn btn-secondary";
    }

    if (currentView === 'rooms') renderApp();
    if (currentView === 'calendar') renderDutyCalendar();
}

function toggleAdminAuth() {
    if (isAdmin) {
        // Logout
        adminToken = '';
        localStorage.removeItem('dorm_admin_token');
        updateAdminUI();
    } else {
        // Open Login Modal
        openAdminLoginModal();
    }
}

function openAdminLoginModal() {
    const errDiv = document.getElementById('adminLoginError');
    if (errDiv) errDiv.style.display = 'none';
    const pwdInput = document.getElementById('adminPasswordInput');
    if (pwdInput) pwdInput.value = '';
    document.getElementById('adminLoginModal').classList.add('active');
    setTimeout(() => { if (pwdInput) pwdInput.focus(); }, 100);
}

function closeAdminLoginModal() {
    document.getElementById('adminLoginModal').classList.remove('active');
}

async function handleAdminLoginSubmit(event) {
    event.preventDefault();
    const pwd = document.getElementById('adminPasswordInput').value.trim();
    const errDiv = document.getElementById('adminLoginError');

    try {
        const res = await fetch('/api/admin/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: pwd })
        });
        const data = await res.json();

        if (res.ok && data.success) {
            adminToken = data.token;
            localStorage.setItem('dorm_admin_token', adminToken);
            closeAdminLoginModal();
            updateAdminUI();
        } else {
            if (errDiv) {
                errDiv.innerText = data.error || window.i18n.t('err_wrong_password');
                errDiv.style.display = 'block';
            }
        }
    } catch (err) {
        console.error("Login error:", err);
        if (errDiv) {
            errDiv.innerText = window.i18n.t('err_connection');
            errDiv.style.display = 'block';
        }
    }
}

function requireAdminPermission(actionCallback) {
    if (!isAdmin) {
        alert(window.i18n.t('admin_require_msg'));
        openAdminLoginModal();
        return;
    }
    actionCallback();
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function getLocalTodayString() {
    const d = new Date();
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// --- VIEW SWITCHING ---
function switchView(view) {
    currentView = view;

    const btnRooms = document.getElementById('viewRoomsBtn');
    const btnCal = document.getElementById('viewCalendarBtn');
    if (btnRooms) btnRooms.classList.toggle('active', view === 'rooms');
    if (btnCal) btnCal.classList.toggle('active', view === 'calendar');

    const floorsEl = document.getElementById('floorsContainer');
    const filtersEl = document.getElementById('roomFilterTabs');
    const searchEl = document.getElementById('searchBoxContainer');
    const calEl = document.getElementById('calendarContainer');
    const calCtrlEl = document.getElementById('calendarControls');

    if (floorsEl) floorsEl.style.display = (view === 'rooms') ? 'block' : 'none';
    if (filtersEl) filtersEl.style.display = (view === 'rooms') ? 'flex' : 'none';
    if (searchEl) searchEl.style.display = (view === 'rooms') ? 'block' : 'none';

    if (calEl) calEl.style.display = (view === 'calendar') ? 'block' : 'none';
    if (calCtrlEl) calCtrlEl.style.display = (view === 'calendar') ? 'flex' : 'none';

    if (view === 'calendar') {
        fetchDutyCalendar();
    } else {
        renderApp();
    }
}

// --- DATA FETCHING ---
async function fetchStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();

        document.getElementById('kpiTotal').innerText = data.total_residents || 0;
        document.getElementById('kpiFloor2').innerText = data.floor2_count || 0;
        document.getElementById('kpiFloor7').innerText = data.floor7_count || 0;
        document.getElementById('kpiTemp').innerText = data.temp_count || 0;
        document.getElementById('kpiWaiting').innerText = data.waiting_count || 0;
        document.getElementById('kpiFreeBeds').innerText = data.free_beds || 0;
    } catch (err) {
        console.error("Error fetching stats:", err);
    }
}

async function fetchFloorsData() {
    try {
        const res = await fetch('/api/floors');
        globalFloorsData = await res.json();

        residentsMap.clear();
        if (globalFloorsData && globalFloorsData.floors) {
            Object.values(globalFloorsData.floors).forEach(rooms => {
                rooms.forEach(rm => {
                    rm.residents.forEach(r => residentsMap.set(r.id, r));
                });
            });
        }
        if (globalFloorsData && globalFloorsData.unassigned) {
            globalFloorsData.unassigned.forEach(r => residentsMap.set(r.id, r));
        }

        if (currentView === 'rooms') renderApp();
    } catch (err) {
        console.error("Error fetching floors data:", err);
    }
}

async function fetchTodayDuty() {
    try {
        const res = await fetch('/api/duty/today');
        const data = await res.json();
        renderTodayDutyBanner(data);
    } catch (err) {
        console.error("Error fetching today duty:", err);
    }
}

function renderTodayDutyBanner(todayData) {
    const container = document.getElementById('todayDutyItems');
    if (!container) return;
    container.innerHTML = '';

    const item = todayData[7];
    if (item) {
        const pillar = document.createElement('div');
        pillar.className = 'duty-pill duty-pill-f7';
        
        const resNames = item.residents.map(r => r.full_name.split(' ')[0]).join(', ') || window.i18n.t('banner_no_residents');

        pillar.innerHTML = `
            <span>${window.i18n.t('banner_floor7')}</span>
            <strong>${window.i18n.t('banner_room', {room: item.room_number})}</strong>
            <span style="opacity:0.8; font-weight:normal;">(${escapeHtml(resNames)})</span>
            ${item.status === 'completed' ? '✅' : ''}
        `;
        container.appendChild(pillar);
    }
}

// --- DUTY CALENDAR LOGIC (FLOOR 7 ONLY) ---
async function fetchDutyCalendar() {
    try {
        const res = await fetch(`/api/duty/calendar?year=${calYear}&month=${calMonth}&floor=7`);
        globalDutyCalendarData = await res.json();
        renderDutyCalendar();
    } catch (err) {
        console.error("Error fetching duty calendar:", err);
    }
}

function changeCalendarMonth(delta) {
    calMonth += delta;
    if (calMonth > 12) {
        calMonth = 1;
        calYear++;
    } else if (calMonth < 1) {
        calMonth = 12;
        calYear--;
    }
    fetchDutyCalendar();
}

function renderDutyCalendar() {
    if (!globalDutyCalendarData) return;

    const monthNamesMap = {
        ru: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        en: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        uz: ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]
    };
    const lang = (window.i18n ? window.i18n.getLanguage() : "ru");
    const monthNames = monthNamesMap[lang] || monthNamesMap.ru;

    const titleEl = document.getElementById('calendarMonthTitle');
    if (titleEl) titleEl.innerText = `${monthNames[calMonth - 1]} ${calYear}`;


    const grid = document.getElementById('calendarDaysGrid');
    if (!grid) return;
    grid.innerHTML = '';

    const firstDay = new Date(calYear, calMonth - 1, 1);
    const daysInMonth = new Date(calYear, calMonth, 0).getDate();
    
    let startingDay = firstDay.getDay() - 1;
    if (startingDay < 0) startingDay = 6;

    for (let i = 0; i < startingDay; i++) {
        const blank = document.createElement('div');
        blank.className = 'cal-day-card empty-day';
        grid.appendChild(blank);
    }

    const todayStr = getLocalTodayString();
    const flItems = globalDutyCalendarData[7] || [];

    for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${calYear}-${String(calMonth).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const isToday = dateStr === todayStr;

        const dayCard = document.createElement('div');
        dayCard.className = `cal-day-card ${isToday ? 'is-today' : ''}`;

        const item = flItems.find(it => it.date === dateStr);

        let dutyItemsHtml = '';
        if (item) {
        const resListStr = item.residents.map(r => r.full_name.split(' ')[0]).join(', ') || window.i18n.t('cal_no_residents');
            const statusTag = {
                'completed': `<span class="cal-status-tag status-completed">${window.i18n.t('cal_status_completed')}</span>`,
                'pending': `<span class="cal-status-tag status-pending">${window.i18n.t('cal_status_pending')}</span>`,
                'skipped': `<span class="cal-status-tag status-skipped">${window.i18n.t('cal_status_skipped')}</span>`,
                'replaced': `<span class="cal-status-tag status-skipped">${window.i18n.t('cal_status_replaced')}</span>`
            }[item.status] || '';

            const editBtnHtml = isAdmin ? `<button type="button" class="btn btn-secondary btn-sm" onclick="openEditDutyModal('${dateStr}', 7, '${item.room_number}', '${item.status}')" title="${window.i18n.t('btn_change_duty_room')}">✏️</button>` : '';

            dutyItemsHtml = `
                <div class="cal-duty-badge f7">
                    <div class="cal-duty-header">
                        <span>${window.i18n.t('cal_day_header_7floor', {room: item.room_number})}</span>
                        ${statusTag}
                    </div>
                    <div class="cal-duty-res">${escapeHtml(resListStr)}</div>
                    <div class="cal-card-actions">
                        ${item.status !== 'completed' ? `<button type="button" class="btn btn-secondary btn-sm" onclick="handleMarkDutyDone('${dateStr}', 7)" title="${window.i18n.t('btn_mark_duty_done')}">✅</button>` : ''}
                        ${editBtnHtml}
                    </div>
                </div>
            `;
        }

        dayCard.innerHTML = `
            <div class="cal-date-num">
                <span>${day}</span>
                ${isToday ? `<span class="today-label">${window.i18n.t('cal_today_label')}</span>` : ''}
            </div>
            <div class="cal-duty-items">
                ${dutyItemsHtml}
            </div>
        `;

        grid.appendChild(dayCard);
    }
}

async function handleMarkDutyDone(dutyDate, floor) {
    try {
        const res = await fetch('/api/duty/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ duty_date: dutyDate, floor: floor, status: 'completed' })
        });
        if (res.ok) {
            fetchTodayDuty();
            fetchDutyCalendar();
        }
    } catch (err) {
        console.error("Error marking duty completed:", err);
    }
}

function openEditDutyModal(dutyDate, floor, currentRoom, currentStatus) {
    requireAdminPermission(() => {
        document.getElementById('dutyModalTitle').innerText = window.i18n.t('duty_modal_title_dynamic', {date: dutyDate});
        document.getElementById('dutyDate').value = dutyDate;
        document.getElementById('dutyFloor').value = 7;
        document.getElementById('dutyDateDisplay').value = window.i18n.t('duty_floor_display', {date: dutyDate});
        document.getElementById('dutyStatus').value = currentStatus || 'pending';
        document.getElementById('dutyNotes').value = '';

        const select = document.getElementById('dutyRoomNumber');
        select.innerHTML = '';

        if (globalFloorsData && globalFloorsData.floors) {
            const rooms = globalFloorsData.floors[7] || [];
            rooms.forEach(rm => {
                const option = document.createElement('option');
                option.value = rm.room_number;
                const resCount = rm.residents.length;
                const emptyTag = resCount === 0 ? window.i18n.t('duty_room_empty_tag') : '';
                option.innerText = window.i18n.t('duty_room_option', {room: rm.room_number, count: resCount, empty: emptyTag});
                if (rm.room_number === currentRoom) option.selected = true;
                select.appendChild(option);
            });
        }

        document.getElementById('dutyModal').classList.add('active');
    });
}

function closeDutyModal() {
    document.getElementById('dutyModal').classList.remove('active');
}

async function handleSaveDuty(event) {
    event.preventDefault();

    const payload = {
        duty_date: document.getElementById('dutyDate').value,
        floor: 7,
        room_number: document.getElementById('dutyRoomNumber').value,
        status: document.getElementById('dutyStatus').value,
        notes: document.getElementById('dutyNotes').value
    };

    try {
        const res = await fetch('/api/duty/assign', {
            method: 'POST',
            headers: getAdminHeaders(),
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            closeDutyModal();
            fetchTodayDuty();
            fetchDutyCalendar();
        } else {
            const errData = await res.json();
            alert(errData.error || window.i18n.t('err_duty_save'));
        }
    } catch (err) {
        console.error("Error saving duty:", err);
    }
}

// --- EXISTING ROOMS LAYOUT LOGIC ---
function setFilter(filter, btn) {
    currentFilter = filter;
    document.querySelectorAll('.filter-tabs .tab-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderApp();
}

function renderApp() {
    if (!globalFloorsData) return;

    const container = document.getElementById('floorsContainer');
    const searchInput = document.getElementById('searchInput');
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
    container.innerHTML = '';

    const floors = globalFloorsData.floors;
    const unassigned = globalFloorsData.unassigned || [];

    [2, 7].forEach(floorNum => {
        if (currentFilter !== 'all' && currentFilter !== 'temp' && currentFilter !== String(floorNum)) {
            return;
        }

        const rooms = floors[floorNum] || [];
        const genderLabel = floorNum === 2 ? window.i18n.t('floor2_badge') : window.i18n.t('floor7_badge');
        const genderBadgeClass = floorNum === 2 ? 'badge-female' : 'badge-male';
        const genderIcon = floorNum === 2 ? 'fa-venus' : 'fa-mars';
        const floorLabel = window.i18n.t('floor_label', {floor: floorNum});
        const roomsCount = window.i18n.t('rooms_count');

        const filteredRooms = rooms.filter(rm => {
            if (currentFilter === 'temp') {
                return rm.residents.some(r => r.status === '14_days');
            }
            if (!query) return true;
            if (rm.room_number.toLowerCase().includes(query)) return true;
            return rm.residents.some(r => 
                r.full_name.toLowerCase().includes(query) || 
                (r.nickname && r.nickname.toLowerCase().includes(query))
            );
        });

        if (filteredRooms.length === 0 && query) return;

        const section = document.createElement('div');
        section.className = 'floor-section';

        section.innerHTML = `
            <div class="section-title">
                <h2>${floorLabel}</h2>
                <span class="floor-badge ${genderBadgeClass}"><i class="fa-solid ${genderIcon}"></i> ${genderLabel} ${roomsCount}</span>
            </div>
            <div class="rooms-grid" id="floor-grid-${floorNum}"></div>
        `;

        container.appendChild(section);
        const grid = section.querySelector(`#floor-grid-${floorNum}`);

        filteredRooms.forEach(room => {
            const card = renderRoomCard(room);
            grid.appendChild(card);
        });
    });

    if (currentFilter === 'all' || currentFilter === 'waiting') {
        const filteredUnassigned = unassigned.filter(r => {
            if (!query) return true;
            return r.full_name.toLowerCase().includes(query) || (r.nickname && r.nickname.toLowerCase().includes(query));
        });

        if (filteredUnassigned.length > 0 || currentFilter === 'waiting') {
            const section = document.createElement('div');
            section.className = 'floor-section';
            section.innerHTML = `
                <div class="section-title">
                    <h2>${window.i18n.t('waiting_section_title')}</h2>
                    <span class="floor-badge badge-female" style="background:var(--red-bg); color:var(--red-accent); border-color:var(--red-border);">
                        <i class="fa-solid fa-user-clock"></i> ${window.i18n.t('waiting_badge', {count: filteredUnassigned.length})}
                    </span>
                </div>
                <div class="rooms-grid">
                    <div class="room-card">
                        <div class="room-card-header">
                            <div class="room-num" style="color:var(--red-accent);">
                                <i class="fa-solid fa-user-slash"></i> ${window.i18n.t('waiting_icon_label')}
                            </div>
                            <span class="occ-pill" style="background:var(--red-bg); color:var(--red-accent);">${window.i18n.t('people_count', {count: filteredUnassigned.length})}</span>
                        </div>
                        <div class="resident-list" id="unassigned-list"></div>
                    </div>
                </div>
            `;
            container.appendChild(section);

            const listEl = section.querySelector('#unassigned-list');
            if (filteredUnassigned.length === 0) {
                listEl.innerHTML = `<div class="bed-empty">${window.i18n.t('waiting_empty')}</div>`;
            } else {
                filteredUnassigned.forEach(res => {
                    listEl.appendChild(renderResidentItem(res));
                });
            }
        }
    }
}

function renderRoomCard(room) {
    const card = document.createElement('div');
    card.className = 'room-card';

    const occ = room.residents.length;
    const cap = room.capacity;
    const isFull = occ >= cap;
    const occClass = isFull ? 'occ-full' : 'occ-space';
    const capLabel = cap === 6 ? window.i18n.t('cap_6') : window.i18n.t('cap_4');

    card.innerHTML = `
        <div class="room-card-header">
            <div class="room-num">
                <i class="fa-solid fa-door-closed" style="color:${room.floor === 2 ? 'var(--pink-accent)' : 'var(--sky-accent)'}"></i>
                ${room.room_number}
                <span class="room-capacity-tag">${capLabel}</span>
            </div>
            <span class="occ-pill ${occClass}">${window.i18n.t('occ_count', {occ, cap})}</span>
        </div>
        <div class="resident-list"></div>
    `;

    const listEl = card.querySelector('.resident-list');

    room.residents.forEach(res => {
        listEl.appendChild(renderResidentItem(res));
    });

    const emptyBeds = cap - occ;
    if (emptyBeds > 0) {
        const emptyEl = document.createElement('div');
        emptyEl.className = 'bed-empty';
        emptyEl.innerHTML = `<i class="fa-solid fa-bed"></i> ${emptyBeds} ${getPluralBeds(emptyBeds)}`;
        listEl.appendChild(emptyEl);
    }

    return card;
}

function renderResidentItem(res) {
    const item = document.createElement('div');
    item.className = `res-item status-${res.status}`;

    const initials = res.full_name.split(' ').map(n => n[0]).slice(0, 2).join('');
    const nickHtml = res.nickname ? `<span class="nick-tag">@${escapeHtml(res.nickname)}</span>` : '';
    const isTempHtml = res.status === '14_days' ? `<span class="nick-tag" style="background:rgba(245,158,11,0.2); color:var(--amber-accent);"><i class="fa-solid fa-clock"></i> ${window.i18n.t('tag_14days')}</span>` : '';

    const adminActionsHtml = isAdmin ? `
        <button type="button" class="btn btn-secondary btn-sm" onclick="openEditResidentModalById(${res.id})" title="Редактировать / Переселить">
            <i class="fa-solid fa-pen"></i>
        </button>
        <button type="button" class="btn btn-danger btn-sm" onclick="handleEvictResidentById(${res.id})" title="Выселить">
            <i class="fa-solid fa-user-minus"></i>
        </button>
    ` : '';

    item.innerHTML = `
        <div class="res-info">
            <div class="res-avatar">${escapeHtml(initials)}</div>
            <div>
                <div class="res-name">${escapeHtml(res.full_name)}</div>
                <div style="display:flex; gap:4px; margin-top:2px;">
                    ${nickHtml}
                    ${isTempHtml}
                </div>
            </div>
        </div>
        <div class="res-actions">
            ${adminActionsHtml}
        </div>
    `;
    return item;
}

function getPluralBeds(num) {
    const lang = window.i18n ? window.i18n.getLanguage() : 'ru';
    if (lang === 'ru') {
        if (num === 1) return 'свободное койко-место';
        if (num >= 2 && num <= 4) return 'свободных койко-места';
        return 'свободных койко-мест';
    } else if (lang === 'uz') {
        return "bo'sh o'rin";
    } else {
        return num === 1 ? 'available bed' : 'available beds';
    }
}

// Modal Handlers
function openAddResidentModal() {
    requireAdminPermission(() => {
        document.getElementById('modalTitle').innerText = window.i18n.t('modal_add_title_dynamic');
        document.getElementById('resId').value = '';
        document.getElementById('resFullName').value = '';
        document.getElementById('resNickname').value = '';
        document.getElementById('resProfileUrl').value = '';
        document.getElementById('resGender').value = 'M';
        document.getElementById('resStatus').value = 'permanent';
        document.getElementById('resNotes').value = '';

        updateRoomOptions();
        document.getElementById('residentModal').classList.add('active');
    });
}

function openEditResidentModalById(resId) {
    requireAdminPermission(() => {
        const res = residentsMap.get(resId);
        if (!res) {
            alert(window.i18n.t('err_not_found'));
            return;
        }
        openEditResidentModal(res);
    });
}

function openEditResidentModal(res) {
    document.getElementById('modalTitle').innerText = window.i18n.t('modal_edit_title_dynamic', {name: res.full_name});
    document.getElementById('resId').value = res.id;
    document.getElementById('resFullName').value = res.full_name;
    document.getElementById('resNickname').value = res.nickname || '';
    document.getElementById('resProfileUrl').value = res.profile_url || '';
    document.getElementById('resGender').value = res.gender;
    document.getElementById('resStatus').value = res.status;
    document.getElementById('resNotes').value = res.notes || '';

    updateRoomOptions(res.room_number);
    document.getElementById('residentModal').classList.add('active');
}

function closeResidentModal() {
    document.getElementById('residentModal').classList.remove('active');
}

function updateRoomOptions(selectedRoom = '') {
    const select = document.getElementById('resRoomNumber');
    const gender = document.getElementById('resGender').value;
    select.innerHTML = `<option value="">${window.i18n.t('room_option_queue')}</option>`;

    if (!globalFloorsData) return;

    const allowedFloor = gender === 'F' ? 2 : 7;
    const rooms = globalFloorsData.floors[allowedFloor] || [];

    rooms.forEach(rm => {
        const occ = rm.residents.length;
        const cap = rm.capacity;
        const isSelected = rm.room_number === selectedRoom;

        const option = document.createElement('option');
        option.value = rm.room_number;
        const extra = cap === 6 ? window.i18n.t('room_option_6beds') : '';
        option.innerText = window.i18n.t('room_option_label', {room: rm.room_number, occ, cap, extra});
        if (isSelected) option.selected = true;
        select.appendChild(option);
    });
}

async function handleSaveResident(event) {
    event.preventDefault();

    const id = document.getElementById('resId').value;
    const payload = {
        full_name: document.getElementById('resFullName').value,
        nickname: document.getElementById('resNickname').value,
        profile_url: document.getElementById('resProfileUrl').value,
        gender: document.getElementById('resGender').value,
        room_number: document.getElementById('resRoomNumber').value,
        status: document.getElementById('resStatus').value,
        notes: document.getElementById('resNotes').value
    };

    const url = id ? `/api/residents/${id}` : '/api/residents';
    const method = id ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, {
            method: method,
            headers: getAdminHeaders(),
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            closeResidentModal();
            fetchStats();
            fetchFloorsData();
            fetchTodayDuty();
        } else {
            const errData = await res.json();
            alert(errData.error || window.i18n.t('err_save'));
        }
    } catch (err) {
        console.error("Error saving resident:", err);
    }
}

async function handleEvictResidentById(resId) {
    requireAdminPermission(async () => {
        const res = residentsMap.get(resId);
        if (!res) return;

        if (!confirm(window.i18n.t('confirm_evict', {name: res.full_name}))) return;

        try {
            const apiRes = await fetch(`/api/residents/${resId}`, {
                method: 'DELETE',
                headers: getAdminHeaders()
            });
            if (apiRes.ok) {
                fetchStats();
                fetchFloorsData();
                fetchTodayDuty();
            } else {
                const errData = await apiRes.json();
                alert(errData.error || window.i18n.t('err_evict'));
            }
        } catch (err) {
            console.error("Error evicting resident:", err);
        }
    });
}

async function openLogsModal() {
    requireAdminPermission(async () => {
        try {
            const res = await fetch('/api/logs', { headers: getAdminHeaders() });
            const logs = await res.json();

            const tbody = document.getElementById('logsTableBody');
            tbody.innerHTML = '';

            logs.forEach(log => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="white-space:nowrap; color:var(--text-muted);">${log.timestamp}</td>
                    <td><strong style="color:var(--primary);">${escapeHtml(log.action)}</strong></td>
                    <td>${escapeHtml(log.details)}</td>
                `;
                tbody.appendChild(tr);
            });

            document.getElementById('logsModal').classList.add('active');
        } catch (err) {
            console.error("Error fetching logs:", err);
        }
    });
}

function closeLogsModal() {
    document.getElementById('logsModal').classList.remove('active');
}

async function exportToExcel() {
    try {
        window.location.href = '/api/download-excel';
    } catch (err) {
        console.error("Error exporting to Excel:", err);
    }
}
