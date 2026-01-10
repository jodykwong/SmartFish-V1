/**
 * SmartFish 模板选择器
 * Story 2-3, 2-4: 模板卡片和预览弹窗
 */

class TemplateSelector {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.templates = [];
        this.selectedTemplateId = null;
        this.onSelect = null;
    }

    async init() {
        await this.loadTemplates();
        this.render();
    }

    async loadTemplates() {
        try {
            const response = await fetch('/api/templates');
            const data = await response.json();
            if (data.success) {
                this.templates = data.templates;
            }
        } catch (error) {
            console.error('加载模板失败:', error);
        }
    }

    render() {
        if (!this.container) return;
        
        this.container.innerHTML = `
            <div class="smartfish-section">
                <div class="smartfish-section-title">
                    📋 选择报告模板
                </div>
                <div class="template-grid" id="template-grid"></div>
            </div>
        `;

        const grid = document.getElementById('template-grid');
        this.templates.forEach(template => {
            grid.appendChild(this.createTemplateCard(template));
        });
    }

    createTemplateCard(template) {
        const card = document.createElement('div');
        card.className = 'template-card';
        card.dataset.templateId = template.id;
        
        card.innerHTML = `
            <div class="template-card-icon">${template.icon || '📋'}</div>
            <div class="template-card-name">${template.name}</div>
            <div class="template-card-tags">${(template.tags || []).slice(0, 2).join(' | ')}</div>
            <div class="template-card-footer">
                <span class="template-card-chapters">${template.chapter_count} 个章节</span>
                <button class="template-preview-btn" data-template-id="${template.id}">预览</button>
            </div>
        `;

        card.addEventListener('click', (e) => {
            if (!e.target.classList.contains('template-preview-btn')) {
                this.selectTemplate(template.id);
            }
        });

        card.querySelector('.template-preview-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            this.showPreview(template.id);
        });

        return card;
    }

    selectTemplate(templateId) {
        this.selectedTemplateId = templateId;
        
        // 更新选中状态
        document.querySelectorAll('.template-card').forEach(card => {
            card.classList.toggle('selected', card.dataset.templateId === templateId);
        });

        if (this.onSelect) {
            this.onSelect(templateId);
        }
    }

    async showPreview(templateId) {
        try {
            const response = await fetch(`/api/templates/${templateId}`);
            const data = await response.json();
            
            if (data.success) {
                this.renderPreviewModal(data.template);
            }
        } catch (error) {
            console.error('加载模板详情失败:', error);
        }
    }

    renderPreviewModal(template) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'template-preview-modal';
        
        const chaptersHtml = (template.chapters || [])
            .map(ch => `<li>${ch}</li>`)
            .join('');

        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <span class="modal-title">${template.icon || '📋'} ${template.name}</span>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <p><strong>适用场景:</strong> ${(template.tags || []).join(' | ')}</p>
                    <p>${template.description || ''}</p>
                    <h4>📑 章节结构 (${template.chapter_count}):</h4>
                    <ul class="chapter-tree">
                        ${chaptersHtml}
                    </ul>
                </div>
                <div class="modal-footer">
                    <button class="btn-default modal-cancel">取消</button>
                    <button class="btn-primary modal-confirm">使用此模板</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // 事件绑定
        modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
        modal.querySelector('.modal-cancel').addEventListener('click', () => modal.remove());
        modal.querySelector('.modal-confirm').addEventListener('click', () => {
            this.selectTemplate(template.id);
            modal.remove();
        });
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.remove();
        });

        // ESC 关闭
        const escHandler = (e) => {
            if (e.key === 'Escape') {
                modal.remove();
                document.removeEventListener('keydown', escHandler);
            }
        };
        document.addEventListener('keydown', escHandler);
    }

    getSelectedTemplate() {
        return this.selectedTemplateId;
    }
}

// 导出
window.TemplateSelector = TemplateSelector;
