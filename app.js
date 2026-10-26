document.addEventListener('DOMContentLoaded', () => {
    loadMatches();
});

// Управление вкладками
function switchTab(tabId) {
    document.getElementById('section-matches').classList.add('hidden');
    document.getElementById('section-stats').classList.add('hidden');
    document.getElementById('section-lab').classList.add('hidden');

    document.getElementById('tab-matches').className = "px-5 py-2 rounded-xl font-bold text-sm bg-emerald-950/85 text-emerald-300 border border-emerald-700/50 hover:bg-emerald-900 transition";
    document.getElementById('tab-stats').className = "px-5 py-2 rounded-xl font-bold text-sm bg-emerald-950/85 text-emerald-300 border border-emerald-700/50 hover:bg-emerald-900 transition";
    document.getElementById('tab-lab').className = "px-5 py-2 rounded-xl font-bold text-sm bg-emerald-950/85 text-emerald-300 border border-emerald-700/50 hover:bg-emerald-900 transition";

    document.getElementById('section-' + tabId).classList.remove('hidden');
    document.getElementById('tab-' + tabId).className = "px-5 py-2 rounded-xl font-bold text-sm bg-emerald-500 text-slate-950 shadow-lg transition";
}

// Загрузка матчей и отрисовка карточек
async function loadMatches() {
    try {
        const response = await fetch('matches.json');
        const matches = await response.json();
        
        const container = document.getElementById('matches-container');
        container.innerHTML = '';

        matches.forEach(match => {
            const card = document.createElement('div');
            card.className = 'board-card rounded-2xl p-6 transition hover:border-emerald-400/60';
            
            const hasStats = match.stats && match.stats.home.xg !== null;

            card.innerHTML = `
                <div class="flex justify-between items-center mb-4 text-xs font-semibold text-emerald-300/80 border-b border-emerald-800/50 pb-2">
                    <span class="uppercase tracking-wider">${match.competition}</span>
                    <span>${match.date}</span>
                </div>
                
                <div class="flex justify-between items-center mb-6">
                    <div class="text-center w-5/12">
                        <h2 class="text-xl font-bold text-slate-100">${match.home_team}</h2>
                        <span class="text-xs text-emerald-400/60">Хозяева</span>
                    </div>
                    <div class="text-xl font-black text-emerald-500/80 tracking-widest">VS</div>
                    <div class="text-center w-5/12">
                        <h2 class="text-xl font-bold text-slate-100">${match.away_team}</h2>
                        <span class="text-xs text-emerald-400/60">Гости</span>
                    </div>
                </div>

                <div class="bg-emerald-950/60 rounded-xl p-4 mb-4 grid grid-cols-2 gap-4 text-center border border-emerald-900">
                    <div>
                        <div class="text-xs text-emerald-300/70 mb-1">Прогноз SOW-X (Голы)</div>
                        <div class="text-lg font-bold text-emerald-400">1.71 : 1.52</div>
                    </div>
                    <div>
                        <div class="text-xs text-emerald-300/70 mb-1">Вероятность 1X2</div>
                        <div class="text-sm font-bold text-blue-300">42% / 26% / 32%</div>
                    </div>
                </div>

                <div class="flex justify-between items-center text-xs text-slate-300 pt-2 border-t border-emerald-900/60">
                    <span>Фактический счёт: <strong class="text-white">${match.home_goals !== null ? match.home_goals + ' : ' + match.away_goals : 'Ожидается'}</strong></span>
                    <span class="px-3 py-1 rounded-lg ${hasStats ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-800 text-slate-400'}">
                        ${hasStats ? '📊 Статистика введена' : '⏳ Статистика пуста'}
                    </span>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Ошибка загрузки матчей:', error);
    }
}
