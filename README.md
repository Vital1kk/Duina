# Duina

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-41AD49?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Windows-0078D6?style=flat-square&logo=windows&logoColor=white" alt="Windows">
  <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black" alt="Linux">
  <img src="https://img.shields.io/badge/macOS-000000?style=flat-square&logo=apple&logoColor=white" alt="macOS">
</p>

Програма для зручної розробки, компіляції та прошивки мікроконтролерів (Arduino, ESP32, STM32).

---

## Зміст
- [Про проєкт](#про-проєкт)
- [Основні можливості](#основні-можливості)
- [Принцип роботи](#принцип-роботи)

---

## Про проєкт

**Duina** — це легкий та швидкий інструмент для роботи з мікроконтролерами. Проєкт створено як лаконічну альтернативу громіздким IDE, із фокусом на високу швидкість завантаження, мінімальне споживання ресурсів та зрозумілий інтерфейс.

> [!NOTE]
> Duina розробляється з акцентом на швидкий старт: від відкриття програми до першої прошивки плати минають лічені секунди.

---

## Основні можливості

* **Швидкий запуск:** Мінімальне навантаження на систему та миттєвий відгук інтерфейсу.
* **Автовизначення:** Автоматичне виявлення підключених плат та активних COM-портів.
* **Кросплатформеність:** Повноцінна підтримка Windows, macOS та Linux.
* **Serial Monitor:** Вбудований монітор послідовного порту для зчитування та відправки даних у реальному часі.

---

## Принцип роботи

Схема взаємодії коду з залізом через Duina:

```mermaid
graph LR
    A[Код C/C++] --> B[Duina IDE]
    B --> C[Компілятор]
    C --> D[Мікроконтролер]
