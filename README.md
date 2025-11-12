# 🎓 Sistema de Catraca com Reconhecimento Facial

Projeto desenvolvido em grupo na faculdade, com o objetivo de criar um **sistema de controle de acesso automatizado** utilizando **reconhecimento facial**.  
O sistema identifica alunos cadastrados, registra seus acessos em um banco de dados e envia comandos a uma **catraca controlada por um ESP32**, permitindo a liberação ou bloqueio de entrada.

---

## 🧠 Funcionalidades
- Reconhecimento facial em tempo real com **OpenCV**  
- Integração com **MySQL** para registro de acessos  
- Controle físico da catraca via **ESP32 (porta serial)**  
- Conversão automática de imagens para o formato compatível  
- Interface web em **PHP** para visualização dos registros  

---

## 🧩 Estrutura do Projeto
| Arquivo | Descrição |
|----------|------------|
| `reconhecimento_opencv_alunos.py` | Código principal de reconhecimento facial e integração com o ESP32 |
| `converter_final.py` | Conversor de imagens para o padrão RGB 8-bit |
| `conexao.php` | Script de conexão com o banco de dados MySQL |
| `index.php` | Interface web para exibir e gerenciar os acessos |

---

## 🛠️ Tecnologias Utilizadas
- **Python** (OpenCV, Pyttsx3, Serial)  
- **PHP**  
- **MySQL**  
- **ESP32**  

---

## 👥 Desenvolvido por
Projeto desenvolvido em grupo por colegas da faculdade de **Análise e Desenvolvimento de Sistemas - UNIMES**,  
com colaboração mútua em todas as etapas de desenvolvimento e integração do sistema.
