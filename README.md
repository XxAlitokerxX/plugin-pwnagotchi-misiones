Create exp.py
Descripción Completa del Plugin
El EXP Plugin está diseñado para integrarse con el sistema del Pwnagotchi y ofrecer un sistema de experiencia y misiones dinámico. Este plugin recompensa al usuario con puntos de experiencia (EXP) por realizar acciones específicas, como capturar handshakes, realizar asociaciones, o completar misiones de inteligencia artificial (IA). También incluye un sistema de misiones que agrega objetivos progresivos para incentivar interacciones y mejorar el comportamiento del Pwnagotchi.

Funcionalidades Clave:
Sistema de Experiencia:

Los usuarios ganan experiencia realizando acciones como:
Asociaciones: Conexiones con puntos de acceso.
Deautenticaciones: Desconexión de dispositivos de redes Wi-Fi.
Captura de handshakes.
Épocas de entrenamiento exitosas de IA.
La experiencia necesaria para subir de nivel aumenta progresivamente, lo que mantiene el sistema desafiante.
Sistema de Misiones:

Cuatro tipos de misiones activas (Handshakes, Deauths, Associations, AI) con recompensas de experiencia específicas.
Los objetivos de las misiones aumentan en dificultad al completarse, hasta alcanzar un límite, tras el cual se reinician.
Las misiones se muestran en pantalla una por una en intervalos para mantener una interfaz limpia.
Interfaz Gráfica:

La experiencia y el nivel se muestran en la pantalla del Pwnagotchi, junto con una barra de progreso visual.
Las misiones activas se presentan de forma rotativa para optimizar el espacio disponible.
Sincronización con la IA de Pwnagotchi:

El plugin interactúa con la IA del Pwnagotchi para recompensar logros en ciclos de aprendizaje automático (épocas exitosas).
Los eventos generados por la IA, como capturas de handshakes y asociaciones, son utilizados para actualizar misiones y experiencia.
Descripción Detallada del Código:
Importación de Módulos:

Se importan módulos estándar de Python (como os, json, y random) y específicos de Pwnagotchi (pwnagotchi.plugins, pwnagotchi.agent, y componentes de UI).
Variables y Constantes Globales:

Se definen multiplicadores para calcular la experiencia obtenida en cada evento (MULTIPLIER_ASSOCIATION, MULTIPLIER_DEAUTH, etc.).
Constantes como el nombre del archivo de guardado (FILE_SAVE) y los mensajes visuales (FACE_LEVELUP) se configuran para uso en todo el plugin.
Clase Mission:

Representa una misión individual con atributos como descripción, objetivo, progreso, recompensa, y límite máximo.
Métodos:
update_progress(value): Actualiza el progreso de la misión.
reset(): Incrementa la dificultad tras completar la misión, hasta un máximo definido.
Clase EXP:

Hereda de plugins.Plugin y representa el núcleo del plugin.
Atributos principales:
exp, lv, exp_tot: Rastrean la experiencia actual, nivel del usuario, y experiencia total acumulada.
missions: Lista de misiones activas.
log: Sistema de registro para depuración y seguimiento.
Métodos importantes:
initialize_missions(): Configura las misiones iniciales con objetivos y recompensas.
save() y load(): Guardan y cargan datos en un archivo JSON.
calcExpNeeded(level): Calcula la experiencia necesaria para alcanzar el siguiente nivel.
exp_check(agent): Verifica si el nivel debe incrementarse y actualiza la interfaz gráfica.
check_mission_completion(type, value): Sincroniza eventos con misiones específicas, asegurando que cada acción se registre correctamente.
on_ui_setup(ui): Configura los elementos gráficos en la pantalla del Pwnagotchi.
on_ui_update(ui): Actualiza la interfaz con el progreso de nivel, experiencia y misiones.
on_association, on_deauthentication, on_handshake, on_ai_best_reward: Métodos conectados a eventos del Pwnagotchi para actualizar experiencia y misiones.
Interacción con el Pwnagotchi:

Los métodos de eventos (on_association, etc.) interactúan directamente con las señales emitidas por el sistema del Pwnagotchi.
Cada vez que ocurre un evento relevante, el plugin actualiza la experiencia acumulada, verifica misiones, y sincroniza con la interfaz gráfica.
Interfaz Gráfica:

Los elementos de la interfaz (nivel, barra de experiencia y misiones) se definen con coordenadas configurables, permitiendo un diseño visual consistente.
Las misiones se muestran de forma rotativa para evitar superposición y mejorar la legibilidad.
Ejemplo de Uso:
Instalación:

Copiar el archivo del plugin a la carpeta correspondiente de plugins en el Pwnagotchi.
Configurar las coordenadas de la interfaz en el archivo de configuración del Pwnagotchi para ajustarlas al diseño deseado.
Funcionamiento:

A medida que el Pwnagotchi interactúa con redes Wi-Fi, se generan eventos que afectan la experiencia y el progreso de misiones.
La interfaz gráfica muestra el nivel, la barra de experiencia, y una misión activa de forma clara.
Seguimiento y Depuración:

Los registros del sistema (log) permiten monitorear el progreso, como niveles alcanzados, misiones completadas, y experiencia acumulada.     

Pasos de Instalación:
Copiar el Archivo del Plugin:

Copie el archivo exp.py a la carpeta de plugins personalizados de su Pwnagotchi.

Alternativamente, puede crear una carpeta específica para sus plugins personalizados y actualizar el archivo de configuración de Pwnagotchi para incluir la ruta.
Configurar Permisos:

Asegúrese de que el archivo del plugin tenga los permisos adecuados ejemplo:
sudo chmod 644 /usr/local/lib/python3.7/dist-packages/pwnagotchi/plugins/exp.py
Si utiliza una carpeta personalizada, asegúrese de que el usuario de Pwnagotchi pueda leer y escribir en la carpeta:

sudo chmod -R 755 /ruta/de/tu/carpeta
Habilitar el Plugin:

Edite el archivo de configuración de Pwnagotchi (generalmente ubicado en /etc/pwnagotchi/config.yml) y añada la siguiente configuración:

main.plugins.exp.enabled: true
main.plugins.exp.lvl_x_coord: 0
main.plugins.exp.lvl_y_coord: 81
main.plugins.exp.exp_x_coord: 38
main.plugins.exp.exp_y_coord: 81
main.plugins.exp.bar_symbols_count: 12
main.plugins.exp.missions_x_coord: 0
main.plugins.exp.missions_y_coord: 32
Reiniciar el Pwnagotchi:

Reinicie el servicio de Pwnagotchi para cargar el plugin:

sudo systemctl restart pwnagotchi
Localizaciones en la Interfaz:
Nivel (Lv):

Coordenadas: (0, 81)
Aparece en la esquina inferior izquierda de la pantalla.
Experiencia (Exp):

Coordenadas: (38, 81)
Barra de progreso visual que muestra la experiencia acumulada en relación al nivel actual.
Misiones (Missions):

Coordenadas: (0, 32)
Las misiones activas se muestran en esta posición, rotando automáticamente para evitar saturar la pantalla.
Con esta configuración, el plugin se integrará perfectamente en la interfaz de Pwnagotchi, proporcionando un sistema visual y dinámico para monitorear el progreso en niveles y misiones.
