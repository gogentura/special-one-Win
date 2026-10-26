document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('matches.json');
        const matches = await response.json();
        
        const container = document.getElementById('matches-container');
        container.innerHTML = '';

        matches.forEach(match => {
            const card = document.createElement('div');
            card.className = 'bg-slate-800 border border-slate-700 rounded-2xl p-6 shadow-xl';
            
            card.innerHTML = `
                <div class="flex justify-between items-center mb-4 text-sm text-slate-400 border-b border-slate-700 pb-2">
                    <span class="font-semibold text-emerald-400">${match.competition}</span>
                    <span>${match.date}</span>
                </div>
                
                <div class="flex justify-between items-center mb-6">
                    <div class="text-center w-5/12">
                        <h2 class="text-xl font-bold">${match.home_team}</h2>
                        <span class="text-xs text-slate-400">Хозяева</span>
                    </div>
                    <div class="text-2xl font-black text-slate-500">VS</div>
                    <div class="text-center w-5/12">
                        <h2 class="text-xl font-bold">${match.away_team}</h2>
                        <span class="text-xs text-slate-400">Гости</span>
                    </div>
                </div>

                <div class="bg-slate-900/60 rounded-xl p-4 mb-4 grid grid-cols-2 gap-4 text-center">
                    <div>
                        <div class="text-xs text-slate-400 mb-1">Фактический счёт</div>
                        <div class="text-lg font-bold text-slate-200">${match.home_goals !== null ? `${match.home_goals} : ${match.away_goals}` : 'Ожидается'}</div>
                    </div>
                    <div>
                        <div class="text-xs text-slate-400 mb-1">Статус xG / Статистики</div>
                        <div class="text-lg font-bold text-emerald-400">${match.stats.home.xg !== null ? 'Заполнено' : 'Пусто'}</div>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Ошибка загрузки матчей:', error);
    }
});
