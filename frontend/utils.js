const API_BASE = '';

async function request(url, options = {}) {
    const defaultOptions = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    
    if (mergedOptions.body && typeof mergedOptions.body === 'object') {
        mergedOptions.body = JSON.stringify(mergedOptions.body);
    }
    
    try {
        const response = await fetch(API_BASE + url, mergedOptions);
        const data = await response.json();
        return { response, data };
    } catch (error) {
        console.error('Request error:', error);
        throw error;
    }
}

function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.main-content') || document.querySelector('.card');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
}

function logout() {
    // 清除用户信息
    localStorage.removeItem('userInfo');
    request('/operate/logout')
        .then(() => {
            window.location.href = '/frontend/login.html';
        })
        .catch(() => {
            window.location.href = '/frontend/login.html';
        });
}

// 获取用户信息并显示在头部
async function loadUserInfo() {
    try {
        console.log('=== loadUserInfo 开始执行 ===');
        
        // 等待一小会儿确保 DOM 完全加载
        await new Promise(resolve => setTimeout(resolve, 50));
        
        // 尝试查找元素
        let headerRightSpan = document.querySelector('.header-right span');
        console.log('查找 .header-right span:', headerRightSpan);
        
        if (!headerRightSpan) {
            console.log('尝试其他选择器...');
            // 尝试查找所有 span
            const allSpans = document.querySelectorAll('span');
            console.log('页面中的 span 元素数量:', allSpans.length);
            // 直接查找包含"欢迎"的 span
            for (let span of allSpans) {
                if (span.textContent && span.textContent.includes('欢迎')) {
                    headerRightSpan = span;
                    console.log('找到包含"欢迎"的 span');
                    break;
                }
            }
        }
        
        let userInfo = localStorage.getItem('userInfo');
        console.log('localStorage 中的 userInfo:', userInfo);
        
        if (!userInfo) {
            console.log('本地没有用户信息，尝试从服务器获取...');
            try {
                const response = await fetch('/operate/userinfo', { credentials: 'include' });
                const data = await response.json();
                console.log('服务器返回:', data);
                if (data.code === 200) {
                    userInfo = JSON.stringify(data.data);
                    localStorage.setItem('userInfo', userInfo);
                    console.log('用户信息已保存到本地');
                }
            } catch (apiError) {
                console.error('调用 API 失败:', apiError);
            }
        }
        
        if (userInfo && headerRightSpan) {
            const user = JSON.parse(userInfo);
            console.log('解析后的用户信息:', user);
            
            // 显示身份：管理员或普通員工
            let roleDisplay = '普通員工';
            if (user) {
                if (user.role === 'admin' || user.role_name === 'admin' || user.role_name === '管理员') {
                    roleDisplay = '管理员';
                } else if (user.role_name && user.role_name !== 'employee') {
                    roleDisplay = user.role_name;
                } else if (user.role === 'employee') {
                    roleDisplay = '普通員工';
                }
            }
            
            console.log('准备显示身份:', roleDisplay);
            headerRightSpan.textContent = `欢迎使用，${roleDisplay}`;
            console.log('=== loadUserInfo 执行完成 ===');
        } else {
            console.log('条件不满足，无法显示用户信息', { userInfo: !!userInfo, element: !!headerRightSpan });
        }
    } catch (error) {
        console.error('加载用户信息失败:', error);
    }
}

function checkLogin() {
    return new Promise((resolve) => {
        request('/operate/logout')
            .then(() => {
                resolve(false);
            })
            .catch(() => {
                resolve(true);
            });
    });
}