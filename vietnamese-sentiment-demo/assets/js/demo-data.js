cat > assets/js/demo-data.js << 'EOF'
// Demo data for Vietnamese Sentiment Analysis

const DEMO_DATA = {
    sampleTexts: {
        positive: [
            "Sản phẩm tuyệt vời! Chất lượng vượt mong đợi, giao hàng nhanh, đóng gói cẩn thận. Shop tư vấn nhiệt tình, phục vụ tận tâm. Tôi rất hài lòng với lần mua sắm này và sẽ tiếp tục ủng hộ shop!",
            "Chất lượng xuất sắc, đúng như mô tả. Giá cả hợp lý, dịch vụ chu đáo. Recommend cho mọi người!",
            "Mình đã mua nhiều lần ở shop này, lần nào cũng hài lòng. Chất lượng ổn định, ship nhanh, phục vụ tốt!"
        ],
        negative: [
            "Rất thất vọng với sản phẩm này! Chất lượng kém, không giống mô tả, màu sắc phai. Giao hàng chậm, đóng gói cẩu thả. Dịch vụ khách hàng thái độ không professional. Không khuyến khích mua!",
            "Sản phẩm tệ, không đáng tiền. Mua về chỉ dùng được vài ngày đã hỏng. Shop không hỗ trợ đổi trả.",
            "Chất lượng dở tệ, không như hình. Giao hàng muộn, không báo trước. Không mua nữa!"
        ],
        neutral: [
            "Sản phẩm bình thường, không có gì đặc biệt. Chất lượng tạm được, phù hợp với mức giá. Giao hàng đúng hẹn, đóng gói ổn. Tổng thể okela.",
            "Cũng được thôi, không quá tốt nhưng cũng không tệ. Giá cả hợp lý.",
            "Bình thường, tạm ổn. Dùng được nhưng không có gì nổi bật."
        ]
    },
    
    mockReviews: [
        {
            id: 1,
            text: "Sản phẩm tuyệt vời, chất lượng tốt!",
            sentiment: "positive",
            confidence: 0.95,
            customer: "Nguyễn Văn A",
            product: "Áo thun nam",
            rating: 5,
            date: "2024-06-24"
        },
        {
            id: 2,
            text: "Không như mong đợi, hơi thất vọng",
            sentiment: "negative", 
            confidence: 0.82,
            customer: "Trần Thị B",
            product: "Váy midi",
            rating: 2,
            date: "2024-06-23"
        },
        {
            id: 3,
            text: "Bình thường, tạm được",
            sentiment: "neutral",
            confidence: 0.68,
            customer: "Lê Văn C", 
            product: "Quần jean",
            rating: 3,
            date: "2024-06-22"
        }
    ],
    
    dashboardMetrics: {
        totalReviews: 1547,
        positiveCount: 986,
        negativeCount: 234,
        neutralCount: 327,
        satisfactionRate: 63.7,
        averageRating: 4.2,
        trendsUp: true,
        alertsCount: 3
    },
    
    productAnalysis: [
        {
            productId: "P001",
            productName: "Áo thun nam basic",
            totalReviews: 156,
            positivePercent: 85,
            negativePercent: 10,
            neutralPercent: 5,
            averageRating: 4.6,
            status: "excellent"
        },
        {
            productId: "P002", 
            productName: "Áo sơ mi nữ",
            totalReviews: 89,
            positivePercent: 45,
            negativePercent: 40,
            neutralPercent: 15,
            averageRating: 3.2,
            status: "needs_attention"
        },
        {
            productId: "P003",
            productName: "Quần jean nam", 
            totalReviews: 234,
            positivePercent: 78,
            negativePercent: 15,
            neutralPercent: 7,
            averageRating: 4.3,
            status: "good"
        }
    ]
};

// Utility functions
const DemoUtils = {
    getRandomSample: (type) => {
        const samples = DEMO_DATA.sampleTexts[type];
        return samples[Math.floor(Math.random() * samples.length)];
    },
    
    formatDate: (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('vi-VN');
    },
    
    getSentimentEmoji: (sentiment) => {
        const emojis = {
            positive: '😊',
            negative: '😞', 
            neutral: '😐'
        };
        return emojis[sentiment] || '😐';
    },
    
    getSentimentColor: (sentiment) => {
        const colors = {
            positive: '#10b981',
            negative: '#ef4444',
            neutral: '#6b7280'
        };
        return colors[sentiment] || '#6b7280';
    }
};

// Export for use in main script
if (typeof window !== 'undefined') {
    window.DEMO_DATA = DEMO_DATA;
    window.DemoUtils = DemoUtils;
}
EOF