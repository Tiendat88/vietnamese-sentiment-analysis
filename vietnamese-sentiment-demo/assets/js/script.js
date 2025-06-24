cat > assets/js/script.js << 'EOF'
// Vietnamese Sentiment Analysis - External Scripts
// File này để dành cho tương lai khi tách JavaScript ra riêng

// Enhanced sentiment analysis with more sophisticated logic
class VietnameseSentimentAnalyzer {
    constructor() {
        this.positiveWords = [
            'tốt', 'đẹp', 'tuyệt', 'hài lòng', 'thích', 'xuất sắc', 
            'tuyệt vời', 'chất lượng', 'nhanh', 'cẩn thận', 'nhiệt tình',
            'ưng ý', 'hoàn hảo', 'recommend', 'khuyến khích', 'ủng hộ'
        ];
        
        this.negativeWords = [
            'tệ', 'dở', 'kém', 'thất vọng', 'không tốt', 'chậm', 
            'cẩu thả', 'không giống', 'phai', 'không khuyến khích',
            'không ưng', 'tồi tệ', 'khó chịu', 'bực mình', 'ghét'
        ];
        
        this.neutralWords = [
            'bình thường', 'tạm được', 'okela', 'không sao', 'được',
            'cũng được', 'tạm oke', 'bình thường', 'trung bình'
        ];
    }
    
    analyze(text) {
        // Advanced analysis logic here
        // This would connect to actual ML model in production
        return this.mockAnalysis(text);
    }
    
    mockAnalysis(text) {
        // Current mock implementation
        // Will be replaced with real API call
        const lowerText = text.toLowerCase();
        let scores = {
            positive: 0,
            negative: 0,
            neutral: 0
        };
        
        // Count word matches
        this.positiveWords.forEach(word => {
            if (lowerText.includes(word)) scores.positive++;
        });
        
        this.negativeWords.forEach(word => {
            if (lowerText.includes(word)) scores.negative++;
        });
        
        this.neutralWords.forEach(word => {
            if (lowerText.includes(word)) scores.neutral++;
        });
        
        // Determine sentiment and confidence
        const maxScore = Math.max(scores.positive, scores.negative, scores.neutral);
        let sentiment = 'neutral';
        let confidence = 0.6;
        
        if (maxScore > 0) {
            if (scores.positive === maxScore) {
                sentiment = 'positive';
                confidence = Math.min(0.7 + scores.positive * 0.1, 0.98);
            } else if (scores.negative === maxScore) {
                sentiment = 'negative';
                confidence = Math.min(0.7 + scores.negative * 0.1, 0.98);
            } else {
                sentiment = 'neutral';
                confidence = 0.6 + Math.random() * 0.2;
            }
        }
        
        // Calculate probabilities
        const total = scores.positive + scores.negative + scores.neutral || 1;
        const probabilities = {
            positive: scores.positive / total,
            negative: scores.negative / total,
            neutral: scores.neutral / total
        };
        
        // Normalize probabilities
        const probSum = probabilities.positive + probabilities.negative + probabilities.neutral;
        if (probSum > 0) {
            Object.keys(probabilities).forEach(key => {
                probabilities[key] = probabilities[key] / probSum;
            });
        }
        
        return {
            sentiment,
            confidence,
            probabilities,
            text,
            wordCounts: scores
        };
    }
}

// Analytics tracking (for future use)
class Analytics {
    static track(eventName, properties = {}) {
        // Google Analytics or custom tracking
        console.log('Analytics:', eventName, properties);
        
        // Example: gtag('event', eventName, properties);
    }
    
    static trackSentimentAnalysis(text, result) {
        this.track('sentiment_analysis', {
            text_length: text.length,
            sentiment: result.sentiment,
            confidence: result.confidence
        });
    }
}

// Export for future modular use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { VietnameseSentimentAnalyzer, Analytics };
}
EOF