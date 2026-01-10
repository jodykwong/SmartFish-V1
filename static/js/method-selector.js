/**
 * SmartFish 分析方法选择器
 * Story 3-3, 3-4: 方法选择器和详情提示
 */

class MethodSelector {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.methods = [];
        this.categories = [];
        this.selectedMethods = new Set();
        this.currentCategory = null;
        this.expanded = false;
    }

    async init() {
        await this.loadCategories();
        await this.loadMethods();
        this.render();
    }

    async loadCategories() {
        try {
            const response = await fetch('/api/method-categories');
            const data = await response.json();
            if (data.success) {
                this.categories = data.categories;
                this.currentCategory = this.categories[0] || null;
            }
        } catch (error) {
            console.error('加载方法分类失败:', error);
        }
    }

    async loadMethods(category = null) {
        try {
            const url = category ? `/api/methods?category=${category}` : '/api/methods';
            const response = await fetch(url);
            const data = await response.json();
            if (data.success) {
                this.methods = data.methods;
            }
        } catch (error) {
            console.error('加载方法列表失败:', error);
        }
    }

    render() {
        if (!this.container) return;

        const categoryLabels = {
            'brainstorming': '头脑风暴',
            'advanced': '高级引导',
            'gamification': '游戏化'
        };

        const tabsHtml = this.categories.map(cat => `
            <button class="method-tab ${cat === this.currentCategory ? 'active' : ''}" 
                    data-category="${cat}">
                ${categoryLabels[cat] || cat}
            </button>
        `).join('');

        const methodsHtml = this.methods
            .filter(m => !this.currentCategory || m.category === this.currentCategory)
            .map(m => this.createMethodItem(m))
            .join('');

        const selectedList = Array.from(this.selectedMethods);
        const selectedHtml = selectedList.length > 0 ? `
            <div class="selected-methods">
                <span>已选: ${selectedList.map(id => {
                    const m = this.methods.find(x => x.id === id);
                    return m ? m.name : id;
                }).join(', ')}</span>
                <button class="clear-methods-btn">清除全部</button>
            </div>
        ` : '';

        this.container.innerHTML = `
            <div class="method-selector ${this.expanded ? 'expanded' : ''}">
                <div class="method-selector-header">
                    <span>🧠 分析方法增强（可选）</span>
                    <span>${this.expanded ? '▲' : '▼'}</span>
                </div>
                <div class="method-selector-body">
                    <div class="method-tabs">${tabsHtml}</div>
                    <div class="method-grid">${methodsHtml}</div>
                    ${selectedHtml}
                </div>
            </div>
        `;

        this.bindEvents();
    }

    createMethodItem(method) {
        const checked = this.selectedMethods.has(method.id) ? 'checked' : '';
        return `
            <div class="method-item">
                <input type="checkbox" id="method-${method.id}" 
                       data-method-id="${method.id}" ${checked}>
                <label for="method-${method.id}">${method.icon || '🧠'} ${method.name}</label>
                <span class="method-help" data-method-id="${method.id}">?
                    <div class="method-tooltip" id="tooltip-${method.id}">
                        <strong>${method.name}</strong><br>
                        ${method.short_description || ''}
                    </div>
                </span>
            </div>
        `;
    }

    bindEvents() {
        // 展开/折叠
        const header = this.container.querySelector('.method-selector-header');
        if (header) {
            header.addEventListener('click', () => {
                this.expanded = !this.expanded;
                this.render();
            });
        }

        // 分类切换
        this.container.querySelectorAll('.method-tab').forEach(tab => {
            tab.addEventListener('click', async (e) => {
                this.currentCategory = e.target.dataset.category;
                await this.loadMethods(this.currentCategory);
                this.render();
            });
        });

        // 方法选择
        this.container.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const methodId = e.target.dataset.methodId;
                if (e.target.checked) {
                    this.selectedMethods.add(methodId);
                } else {
                    this.selectedMethods.delete(methodId);
                }
                this.render();
            });
        });

        // 清除全部
        const clearBtn = this.container.querySelector('.clear-methods-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.selectedMethods.clear();
                this.render();
            });
        }

        // 加载方法详情（悬停时）
        this.container.querySelectorAll('.method-help').forEach(help => {
            help.addEventListener('mouseenter', async (e) => {
                const methodId = e.target.dataset.methodId;
                await this.loadMethodDetail(methodId);
            });
        });
    }

    async loadMethodDetail(methodId) {
        try {
            const response = await fetch(`/api/methods/${methodId}`);
            const data = await response.json();
            if (data.success) {
                const tooltip = document.getElementById(`tooltip-${methodId}`);
                if (tooltip) {
                    const method = data.method;
                    tooltip.innerHTML = `
                        <strong>${method.name}</strong><br>
                        ${method.full_description || method.short_description || ''}<br>
                        <em>适合: ${(method.suitable_for || []).join(', ')}</em>
                    `;
                }
            }
        } catch (error) {
            console.error('加载方法详情失败:', error);
        }
    }

    getSelectedMethods() {
        return Array.from(this.selectedMethods);
    }
}

// 导出
window.MethodSelector = MethodSelector;
