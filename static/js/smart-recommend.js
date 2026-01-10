/**
 * SmartFish 智能推荐
 * Story 5-1, 5-2: 模板推荐逻辑和标记展示
 */

class SmartRecommend {
    constructor() {
        this.templates = [];
        this.debounceTimer = null;
    }

    async init(templates) {
        this.templates = templates;
    }

    /**
     * 根据用户输入推荐模板
     * @param {string} query 用户输入
     * @returns {string|null} 推荐的模板ID
     */
    recommend(query) {
        if (!query || query.length < 2) return null;

        const queryLower = query.toLowerCase();
        let bestMatch = null;
        let bestScore = 0;

        for (const template of this.templates) {
            const keywords = template.recommended_keywords || [];
            let score = 0;

            for (const keyword of keywords) {
                if (queryLower.includes(keyword.toLowerCase())) {
                    score += keyword.length; // 更长的关键词权重更高
                }
            }

            // 也检查模板名称和标签
            if (template.name && queryLower.includes(template.name.toLowerCase())) {
                score += 10;
            }
            for (const tag of (template.tags || [])) {
                if (queryLower.includes(tag.toLowerCase())) {
                    score += 5;
                }
            }

            if (score > bestScore) {
                bestScore = score;
                bestMatch = template.id;
            }
        }

        return bestScore > 0 ? bestMatch : null;
    }

    /**
     * 防抖处理用户输入
     */
    debounceRecommend(query, callback, delay = 300) {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            const recommendedId = this.recommend(query);
            callback(recommendedId);
        }, delay);
    }
}

window.SmartRecommend = SmartRecommend;
