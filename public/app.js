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
        if (isAdmin) {
            authBtn.innerHTML = `<i class="fa-solid fa-right-from-bracket"></i> Выйти из админа`;
            authBtn.className = "btn btn-danger";
        } else {
            authBtn.innerHTML = `<i class="fa-solid fa-lock"></i> Вход для админа`;
            authBtn.className = "btn btn-secondary";
        }
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
                errDiv.innerText = data.error || 'Неверный пароль администратора';
                errDiv.style.display = 'block';
            }
        }
    } catch (err) {
        console.error("Login error:", err);
        if (errDiv) {
            errDiv.innerText = 'Ошибка соединения с сервером';
            errDiv.style.display = 'block';
        }
    }
}

function requireAdminPermission(actionCallback) {
    if (!isAdmin) {
        alert("🔒 Эта функция доступна только Администратору. Пожалуйста, войдите с помощью пароля администратора.");
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
        
        const resNames = item.residents.map(r => r.full_name.split(' ')[0]).join(', ') || 'Нет жильцов';

        pillar.innerHTML = `
            <span>🔷 7 Этаж:</span>
            <strong>Комната ${item.room_number}</strong>
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
            const resListStr = item.residents.map(r => r.full_name.split(' ')[0]).join(', ') || 'Без жильцов';
            const statusTag = {
                'completed': '<span class="cal-status-tag status-completed">✅ Выполнено</span>',
                'pending': '<span class="cal-status-tag status-pending">⏳ Запланировано</span>',
                'skipped': '<span class="cal-status-tag status-skipped">⚠️ Пропущено</span>',
                'replaced': '<span class="cal-status-tag status-skipped">🔄 Заменено</span>'
            }[item.status] || '';

            const editBtnHtml = isAdmin ? `<button type="button" class="btn btn-secondary btn-sm" onclick="openEditDutyModal('${dateStr}', 7, '${item.room_number}', '${item.status}')" title="Переназначить комнату">✏️</button>` : '';

            dutyItemsHtml = `
                <div class="cal-duty-badge f7">
                    <div class="cal-duty-header">
                        <span>🔷 Комн. ${item.room_number}</span>
                        ${statusTag}
                    </div>
                    <div class="cal-duty-res">${escapeHtml(resListStr)}</div>
                    <div class="cal-card-actions">
                        ${item.status !== 'completed' ? `<button type="button" class="btn btn-secondary btn-sm" onclick="handleMarkDutyDone('${dateStr}', 7)" title="Отметить выполненным">✅</button>` : ''}
                        ${editBtnHtml}
                    </div>
                </div>
            `;
        }

        dayCard.innerHTML = `
            <div class="cal-date-num">
                <span>${day}</span>
                ${isToday ? '<span class="today-label">СЕГОДНЯ</span>' : ''}
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
        document.getElementById('dutyModalTitle').innerText = `Дежурство на ${dutyDate}`;
        document.getElementById('dutyDate').value = dutyDate;
        document.getElementById('dutyFloor').value = 7;
        document.getElementById('dutyDateDisplay').value = `${dutyDate} (7 этаж)`;
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
                option.innerText = `Комната ${rm.room_number} (${resCount} чел.) ${resCount === 0 ? '[Пустая]' : ''}`;
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
            alert(errData.error || "Ошибка сохранения дежурства.");
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
        const genderLabel = floorNum === 2 ? 'Женский блок' : 'Мужской блок';
        const genderBadgeClass = floorNum === 2 ? 'badge-female' : 'badge-male';
        const genderIcon = floorNum === 2 ? 'fa-venus' : 'fa-mars';

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
                <h2>${floorNum} Этаж</h2>
                <span class="floor-badge ${genderBadgeClass}"><i class="fa-solid ${genderIcon}"></i> ${genderLabel} (14 комнат)</span>
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
                    <h2>В очереди / Без комнаты</h2>
                    <span class="floor-badge badge-female" style="background:var(--red-bg); color:var(--red-accent); border-color:var(--red-border);">
                        <i class="fa-solid fa-user-clock"></i> Список ожидания (${filteredUnassigned.length} чел.)
                    </span>
                </div>
                <div class="rooms-grid">
                    <div class="room-card">
                        <div class="room-card-header">
                            <div class="room-num" style="color:var(--red-accent);">
                                <i class="fa-solid fa-user-slash"></i> Ожидающие
                            </div>
                            <span class="occ-pill" style="background:var(--red-bg); color:var(--red-accent);">${filteredUnassigned.length} чел.</span>
                        </div>
                        <div class="resident-list" id="unassigned-list"></div>
                    </div>
                </div>
            `;
            container.appendChild(section);

            const listEl = section.querySelector('#unassigned-list');
            if (filteredUnassigned.length === 0) {
                listEl.innerHTML = `<div class="bed-empty">В очереди никого нет</div>`;
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
    const capLabel = cap === 6 ? '6 мест' : '4 места';

    card.innerHTML = `
        <div class="room-card-header">
            <div class="room-num">
                <i class="fa-solid fa-door-closed" style="color:${room.floor === 2 ? 'var(--pink-accent)' : 'var(--sky-accent)'}"></i>
                ${room.room_number}
                <span class="room-capacity-tag">${capLabel}</span>
            </div>
            <span class="occ-pill ${occClass}">${occ} / ${cap} чел.</span>
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
    const isTempHtml = res.status === '14_days' ? `<span class="nick-tag" style="background:rgba(245,158,11,0.2); color:var(--amber-accent);"><i class="fa-solid fa-clock"></i> 14 дней</span>` : '';

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
    if (num === 1) return 'свободное койко-место';
    if (num >= 2 && num <= 4) return 'свободных койко-места';
    return 'свободных койко-мест';
}

// Modal Handlers
function openAddResidentModal() {
    requireAdminPermission(() => {
        document.getElementById('modalTitle').innerText = 'Заселение нового жильца';
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
            alert("Жилец не найден.");
            return;
        }
        openEditResidentModal(res);
    });
}

function openEditResidentModal(res) {
    document.getElementById('modalTitle').innerText = `Редактирование: ${res.full_name}`;
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
    select.innerHTML = `<option value="">-- В очередь (Без комнаты) --</option>`;

    if (!globalFloorsData) return;

    const allowedFloor = gender === 'F' ? 2 : 7;
    const rooms = globalFloorsData.floors[allowedFloor] || [];

    rooms.forEach(rm => {
        const occ = rm.residents.length;
        const cap = rm.capacity;
        const isSelected = rm.room_number === selectedRoom;

        const option = document.createElement('option');
        option.value = rm.room_number;
        option.innerText = `Комната ${rm.room_number} (${occ}/${cap} чел.) ${cap === 6 ? '[6-местная]' : ''}`;
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
            alert(errData.error || "Ошибка сохранения данных.");
        }
    } catch (err) {
        console.error("Error saving resident:", err);
    }
}

async function handleEvictResidentById(resId) {
    requireAdminPermission(async () => {
        const res = residentsMap.get(resId);
        if (!res) return;

        if (!confirm(`Вы действительно хотите выселить жильца "${res.full_name}"?`)) return;

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
                alert(errData.error || "Ошибка выселения.");
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
