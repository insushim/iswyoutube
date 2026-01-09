const { onRequest } = require('firebase-functions/v2/https');
const { defineSecret } = require('firebase-functions/params');
const admin = require('firebase-admin');
const { GoogleGenerativeAI } = require('@google/generative-ai');

admin.initializeApp();

// Secret Manager에서 API 키 가져오기 (절대 노출 안됨)
const geminiApiKey = defineSecret('GEMINI_API_KEY');

// Gemini API 호출 (API 키는 서버에서만 사용)
exports.callGemini = onRequest(
    { cors: true, secrets: [geminiApiKey] },
    async (req, res) => {
        try {
            if (req.method !== 'POST') {
                return res.status(405).json({ error: 'Method not allowed' });
            }

            const { prompt, temperature = 0.7, maxTokens = 8192 } = req.body;

            if (!prompt) {
                return res.status(400).json({ error: 'Prompt is required' });
            }

            const apiKey = geminiApiKey.value();

            if (!apiKey) {
                console.error('Gemini API key not configured');
                return res.status(500).json({ error: 'API key not configured' });
            }

            const genAI = new GoogleGenerativeAI(apiKey);
            const model = genAI.getGenerativeModel({
                model: 'gemini-2.0-flash',
                generationConfig: {
                    temperature: temperature,
                    maxOutputTokens: maxTokens,
                }
            });

            const result = await model.generateContent(prompt);
            const response = await result.response;
            const text = response.text();

            res.status(200).json({
                success: true,
                data: {
                    candidates: [{
                        content: {
                            parts: [{ text: text }]
                        }
                    }]
                },
                model: 'gemini-2.0-flash'
            });

        } catch (error) {
            console.error('Gemini API error:', error.message);
            res.status(500).json({
                success: false,
                error: error.message
            });
        }
    }
);

// 스크립트 생성 전용 엔드포인트
exports.generateScript = onRequest(
    { cors: true, secrets: [geminiApiKey] },
    async (req, res) => {
        try {
            if (req.method !== 'POST') {
                return res.status(405).json({ error: 'Method not allowed' });
            }

            const { prompt, temperature = 0.8 } = req.body;

            if (!prompt) {
                return res.status(400).json({ error: 'Prompt is required' });
            }

            const apiKey = geminiApiKey.value();

            if (!apiKey) {
                return res.status(500).json({ error: 'API key not configured' });
            }

            const genAI = new GoogleGenerativeAI(apiKey);
            const model = genAI.getGenerativeModel({
                model: 'gemini-2.0-flash',
                generationConfig: {
                    temperature: temperature,
                    maxOutputTokens: 16384,
                }
            });

            const result = await model.generateContent(prompt);
            const response = await result.response;
            const text = response.text();

            res.status(200).json({
                success: true,
                data: {
                    candidates: [{
                        content: {
                            parts: [{ text: text }]
                        }
                    }]
                },
                model: 'gemini-2.0-flash'
            });

        } catch (error) {
            console.error('Script generation error:', error.message);
            res.status(500).json({
                success: false,
                error: error.message
            });
        }
    }
);
