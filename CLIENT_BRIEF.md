# Client Brief: Agente de Voz Conversacional con Python y asyncio

## Descripción del Proyecto
Construir un agente de voz conversacional mínimo en Python puro usando 
asyncio para entender profundamente la arquitectura detrás de frameworks 
como Pipecat y LiveKit Agents.

## Objetivos
- Comprender la arquitectura de agentes de voz en tiempo real
- Implementar un pipeline completo sin depender de frameworks externos
- Crear una base de conocimiento para futuros proyectos con Pipecat/LiveKit

## Funcionalidades Principales
### Backend
- Captura de audio desde micrófono usando asyncio
- Transcripción de voz a texto (Speech-to-Text)
- Procesamiento con LLM para generar respuestas
- Síntesis de texto a voz (Text-to-Speech)
- Reproducción de audio por altavoz

### Frontend
- Interfaz de usuario para iniciar/detener conversación
- Visualización de transcripciones en tiempo real
- Indicadores de estado del pipeline

## Tecnologías
- Python 3.10+
- asyncio para el loop principal
- Librerías de audio (PyAudio, sounddevice)
- APIs de STT/TTS/LLM (a definir)

## Criterios de Éxito
- El pipeline funciona de extremo a extremo
- El código es didáctico y bien documentado
- La latencia es aceptable para una conversación fluida