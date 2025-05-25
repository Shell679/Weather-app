function formatDate(dateString) {
    const date = new Date(dateString);
    const days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
    const months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                    'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];

    return {
        dayName: days[date.getDay()],
        fullDate: `${date.getDate()} ${months[date.getMonth()]}`
    };
}



document.getElementById("search-btn").addEventListener("click", async () => {
    const city = document.getElementById("city-input").value;
    try {
        const response = await fetch(`http://localhost:8000/api/weather?request_city=${encodeURIComponent(city)}`);
        if (!response.ok) {
            throw new Error("Ошибка при получении данных");
        }
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error(error);
    }

    const verdictIconMap = {
    "Ясно": "sunny",
    "Преимущественно ясно": "sunny",
    "Переменная облачность": "cloudy",
    "Пасмурно": "cloud",
    "Лёгкая морось": "rain",
    "Умеренная морось": "rain",
    "Сильная морось": "rain",
    "Слабый дождь": "rain",
    "Умеренный дождь": "rain",
    "Сильный дождь": "heavy-rain",
    "Слабый ливень": "heavy-rain",
    "Ливень": "heavy-rain",
    "Сильный ливень": "heavy-rain",
    "Гроза": "heavy-rain",
    "Снег": "snow",
    "Изморозь": "snow",
    "Туман": "cloudy"
};

    const res = await fetch(`http://localhost:8000/api/weather?request_city=${city}`);
    if (!res.ok) {
        alert("Город не найден!");
        return;
    }

    function getWeatherIcon(verdict) {
    const iconKey = verdictIconMap[verdict];
    return iconKey ? `images/${iconKey}.png` : "images/default.png";
}

    const data = await res.json();
    const section = document.getElementById('weather-result');
    section.classList.remove('hidden');
    section.innerHTML = '';

    const currentTempDiv = document.getElementById('current-temp');

    currentTempDiv.classList.remove('hidden');
    currentTempDiv.textContent = `На данный момент температура: ${data.current_temperature}°C`;

    requestAnimationFrame(() => {
      currentTempDiv.classList.add('visible');
    });

    data.forecast.forEach((day, index) => {
    const card = document.createElement('div');
    card.className = 'weather-card';
    card.style.animationDelay = `${index * 0.2}s`;
    const { dayName, fullDate } = formatDate(day.date);
    card.innerHTML = `
        <img src="${getWeatherIcon(day.verdict)}" alt="Иконка" />
        <div class="day-date">
            <div class="day-name">${dayName}</div>
            <div class="date">${fullDate}</div>
        </div>
        <div class="temperature">Макс: ${day.temperature_max}°C</div>
        <div class="temperature">Мин: ${day.temperature_min}°C</div>
        <div>Осадки: ${day.precipitation} мм</div>
        <div class="description">${day.verdict}</div>
    `;
    section.appendChild(card);
    });
});
