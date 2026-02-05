const API_URL = window.location.origin + '/api/v1/tasks';

// Элементы DOM
const taskForm = document.getElementById('taskForm');
const tasksContainer = document.getElementById('tasksContainer');
const errorDiv = document.getElementById('error');
const successDiv = document.getElementById('success');
const apiUrlSpan = document.getElementById('apiUrl');
const taskCountSpan = document.getElementById('taskCount');

// Показать сообщение об ошибке
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    successDiv.style.display = 'none';
    
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Показать сообщение об успехе
function showSuccess(message) {
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    errorDiv.style.display = 'none';
    
    setTimeout(() => {
        successDiv.style.display = 'none';
    }, 3000);
}

// Получить CSS класс для статуса
function getStatusClass(status) {
    switch(status) {
        case 'active': return 'status status-active';
        case 'completed': return 'status status-completed';
        case 'pending': return 'status status-pending';
        default: return 'status';
    }
}

// Получить русское название статуса
function getStatusText(status) {
    const statusMap = {
        'active': 'Активная',
        'completed': 'Завершена', 
        'pending': 'В ожидании'
    };
    return statusMap[status] || status;
}

// Форматирование даты
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU');
}

// Создать карточку задачи
function createTaskCard(task) {
    return `
        <div class="task-card" data-id="${task.id}">
            <div class="task-title">${task.title}</div>
            ${task.description ? `<div class="task-description">${task.description}</div>` : ''}
            <div class="task-meta">
                <div>
                    <span class="${getStatusClass(task.status)}">
                        ${getStatusText(task.status)}
                    </span>
                </div>
                <div>${formatDate(task.created_at)}</div>
            </div>
            <div class="controls">
                <button onclick="updateTaskStatus(${task.id}, 'completed')" 
                        class="btn btn-small" ${task.status === 'completed' ? 'disabled' : ''}>
                    ✅ Завершить
                </button>
                <button onclick="deleteTask(${task.id})" class="btn btn-small btn-delete">
                    🗑️ Удалить
                </button>
            </div>
        </div>
    `;
}

// Загрузить все задачи
async function loadTasks() {
    try {
        tasksContainer.innerHTML = '<div class="loading">Загрузка задач...</div>';
        
        // ИСПРАВЛЕНО: правильный путь
        const response = await fetch(`${API_URL}/tasks/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const tasks = Array.isArray(data) ? data : (data.items || []);
        
        if (tasks.length === 0) {
            tasksContainer.innerHTML = '<div class="loading">Задач пока нет. Добавьте первую!</div>';
            taskCountSpan.textContent = '0';
            return;
        }
        
        tasksContainer.innerHTML = '<div class="tasks-grid"></div>';
        const grid = tasksContainer.querySelector('.tasks-grid');
        
        // Сортируем по дате создания (новые первыми)
        tasks.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        
        tasks.forEach(task => {
            grid.innerHTML += createTaskCard(task);
        });
        
        taskCountSpan.textContent = tasks.length.toString();
        
    } catch (error) {
        console.error('Error loading tasks:', error);
        tasksContainer.innerHTML = `<div class="error">Ошибка загрузки задач: ${error.message}</div>`;
    }
}

// Создать новую задачу
async function createTask(taskData) {
    try {
        // ИСПРАВЛЕНО: правильный путь
        const response = await fetch(`${API_URL}/tasks/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const newTask = await response.json();
        showSuccess(`Задача "${newTask.title}" создана!`);
        taskForm.reset();
        loadTasks();
        
    } catch (error) {
        console.error('Error creating task:', error);
        showError(`Ошибка создания задачи: ${error.message}`);
    }
}

// Обновить статус задачи
async function updateTaskStatus(taskId, status) {
    try {
        // ИСПРАВЛЕНО: правильный путь
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        showSuccess('Статус задачи обновлен!');
        loadTasks();
        
    } catch (error) {
        console.error('Error updating task:', error);
        showError(`Ошибка обновления задачи: ${error.message}`);
    }
}

// Удалить задачу
async function deleteTask(taskId) {
    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) {
        return;
    }
    
    try {
        // ИСПРАВЛЕНО: правильный путь
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        showSuccess('Задача удалена!');
        loadTasks();
        
    } catch (error) {
        console.error('Error deleting task:', error);
        showError(`Ошибка удаления задачи: ${error.message}`);
    }
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    // Показать URL API
    apiUrlSpan.textContent = API_URL;
    
    // Загрузить задачи при загрузке страницы
    loadTasks();
    
    // Обработка формы
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = document.getElementById('title').value.trim();
        if (!title) {
            showError('Название задачи обязательно!');
            return;
        }
        
        const taskData = {
            title: title,
            description: document.getElementById('description').value.trim(),
            status: document.getElementById('status').value
        };
        
        await createTask(taskData);
    });
});

// Экспорт функций для использования в HTML
window.loadTasks = loadTasks;
window.updateTaskStatus = updateTaskStatus;
window.deleteTask = deleteTask;