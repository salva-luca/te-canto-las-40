// Votación de "Te canto las 40". Se usa en script.google.com (Apps Script).
// 1) Ahora: ejecutar crearFormulario. Crea el form con opciones de prueba y muestra los links.
// 2) Después del karaoke: reemplazar OPCIONES con los nombres reales y ejecutar cargarOpciones.

const TITULO = 'Te canto las 40: votación';

const OPCIONES = {
  "Mejor cantante": ["Agus", "Ale", "Ayerbe", "Ayma", "Crista", "Fede Max", "Felipe", "Gigi", "Guille", "Iara", "Javi", "Julie", "Lu", "Maca", "Manu", "Martín", "Maru", "Mili", "Nati", "Pato", "Salva", "Santi", "Simona", "Sofi"],
  "Mejor show": ["Maru y Agus: Like a Prayer", "Ale: Crazy Little Thing Called Love", "Felipe: Un amor (Lali)", "Agus: Porque yo te amo (Sandro)", "Los dos pitis (Martín y Sofi): Todo sigue igual", "Crista: Sweet Dreams", "Maca: Hay que venir al sur", "Ale y Salva: You Shook Me All Night Long", "Agus y las banana: Maldita noche", "Maru y Salva: Bachata rosa", "Agus y Martín: Lo mejor del amor", "Ale y Salva: Dejaría todo", "Crista y Lu: Just a Girl", "Crista, Salva y Agus: No podrás", "Ayma, Guille, Julie y Simona: Por qué te vas", "Maru, Nati y Mili: No te creas tan importante", "Maca y Crista: Crazy in Love", "Maru y Sofi: Imán", "Iara, Javi y Fede Max: Tiny Dancer", "Salva, Lu y Maca: Fuiste", "Iara, Ale y Fede Max: Satisfaction", "Maca, Crista y Lu: Toxic", "Nati, Ale, Salva y Martín: Fuego de noche", "Ayerbe y Sofi: Isla", "Lu, Maru y Javi: Gangsta's Paradise", "Maru, Lu y Javi: Kiss from a Rose", "Maca, Santi y Sofi: Al siguiente nivel", "Full band: Dos días en la vida", "Ale, Nati y Salva: Por amarte así", "Maru, Crista y Nati: Estoy aquí", "Maca y Crista: Piel morena", "Full band: Total Eclipse of the Heart", "Full band: La incondicional", "Full band: Amor (Cristian Castro)", "Gigi, Pato, Manu y Martín: Obsesionario en la mayor", "Iara y Maru: Ain't Over 'til It's Over", "Lu, Salva y Maru: Sin disfraz", "Agus y Martín: Pronta entrega", "Full band: It Must Have Been Love", "Agus, Martín y Nati: Una calle nos separa", "Full band: Canción de despedida"],
  "Mejor personificación": ["Agus", "Ale", "Ayerbe", "Ayma", "Crista", "Fede Max", "Felipe", "Gigi", "Guille", "Iara", "Javi", "Julie", "Lu", "Maca", "Manu", "Martín", "Maru", "Mili", "Nati", "Pato", "Salva", "Santi", "Simona", "Sofi"],
  "Mejor dúo o grupo": ["Maru y Agus: Like a Prayer", "Los dos pitis (Martín y Sofi): Todo sigue igual", "Ale y Salva: You Shook Me All Night Long", "Agus y las banana: Maldita noche", "Maru y Salva: Bachata rosa", "Agus y Martín: Lo mejor del amor", "Ale y Salva: Dejaría todo", "Crista y Lu: Just a Girl", "Crista, Salva y Agus: No podrás", "Ayma, Guille, Julie y Simona: Por qué te vas", "Maru, Nati y Mili: No te creas tan importante", "Maca y Crista: Crazy in Love", "Maru y Sofi: Imán", "Iara, Javi y Fede Max: Tiny Dancer", "Salva, Lu y Maca: Fuiste", "Iara, Ale y Fede Max: Satisfaction", "Maca, Crista y Lu: Toxic", "Nati, Ale, Salva y Martín: Fuego de noche", "Ayerbe y Sofi: Isla", "Lu, Maru y Javi: Gangsta's Paradise", "Maru, Lu y Javi: Kiss from a Rose", "Maca, Santi y Sofi: Al siguiente nivel", "Full band: Dos días en la vida", "Ale, Nati y Salva: Por amarte así", "Maru, Crista y Nati: Estoy aquí", "Maca y Crista: Piel morena", "Full band: Total Eclipse of the Heart", "Full band: La incondicional", "Full band: Amor (Cristian Castro)", "Gigi, Pato, Manu y Martín: Obsesionario en la mayor", "Iara y Maru: Ain't Over 'til It's Over", "Lu, Salva y Maru: Sin disfraz", "Agus y Martín: Pronta entrega", "Full band: It Must Have Been Love", "Agus, Martín y Nati: Una calle nos separa", "Full band: Canción de despedida"],
  "Mejor coreografía": ["Maru y Agus: Like a Prayer", "Ale: Crazy Little Thing Called Love", "Felipe: Un amor (Lali)", "Agus: Porque yo te amo (Sandro)", "Los dos pitis (Martín y Sofi): Todo sigue igual", "Crista: Sweet Dreams", "Maca: Hay que venir al sur", "Ale y Salva: You Shook Me All Night Long", "Agus y las banana: Maldita noche", "Maru y Salva: Bachata rosa", "Agus y Martín: Lo mejor del amor", "Ale y Salva: Dejaría todo", "Crista y Lu: Just a Girl", "Crista, Salva y Agus: No podrás", "Ayma, Guille, Julie y Simona: Por qué te vas", "Maru, Nati y Mili: No te creas tan importante", "Maca y Crista: Crazy in Love", "Maru y Sofi: Imán", "Iara, Javi y Fede Max: Tiny Dancer", "Salva, Lu y Maca: Fuiste", "Iara, Ale y Fede Max: Satisfaction", "Maca, Crista y Lu: Toxic", "Nati, Ale, Salva y Martín: Fuego de noche", "Ayerbe y Sofi: Isla", "Lu, Maru y Javi: Gangsta's Paradise", "Maru, Lu y Javi: Kiss from a Rose", "Maca, Santi y Sofi: Al siguiente nivel", "Full band: Dos días en la vida", "Ale, Nati y Salva: Por amarte así", "Maru, Crista y Nati: Estoy aquí", "Maca y Crista: Piel morena", "Full band: Total Eclipse of the Heart", "Full band: La incondicional", "Full band: Amor (Cristian Castro)", "Gigi, Pato, Manu y Martín: Obsesionario en la mayor", "Iara y Maru: Ain't Over 'til It's Over", "Lu, Salva y Maru: Sin disfraz", "Agus y Martín: Pronta entrega", "Full band: It Must Have Been Love", "Agus, Martín y Nati: Una calle nos separa", "Full band: Canción de despedida"],
};

function crearFormulario() {
  const form = FormApp.create(TITULO);
  form.setDescription('Elegí a tus favoritos en cada categoría. Podés saltear las que quieras.');
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false); // si fuera true, cada invitado tendría que entrar con Google
  form.setShowLinkToRespondAgain(false);
  form.setAllowResponseEdits(false);
  form.setProgressBar(false);
  form.setConfirmationMessage('¡Gracias por votar! Los ganadores se anuncian en un ratito.');
  Object.keys(OPCIONES).forEach(function (categoria) {
    form.addMultipleChoiceItem()
      .setTitle(categoria)
      .setChoiceValues(OPCIONES[categoria])
      .setRequired(false);
  });
  try { form.setPublished(true); } catch (e) { /* cuentas donde el form ya nace publicado */ }
  PropertiesService.getScriptProperties().setProperty('FORM_ID', form.getId());
  Logger.log('Link para votar (va en el QR): ' + form.getPublishedUrl());
  Logger.log('Link para editar y ver resultados: ' + form.getEditUrl());
}

function cargarOpciones() {
  const id = PropertiesService.getScriptProperties().getProperty('FORM_ID');
  if (!id) throw new Error('Primero ejecutá crearFormulario.');
  const form = FormApp.openById(id);
  const faltan = Object.keys(OPCIONES);
  form.getItems(FormApp.ItemType.MULTIPLE_CHOICE).forEach(function (item) {
    const lista = OPCIONES[item.getTitle()];
    if (!lista) return;
    item.asMultipleChoiceItem().setChoiceValues(lista);
    faltan.splice(faltan.indexOf(item.getTitle()), 1);
  });
  if (faltan.length) Logger.log('No encontré estas categorías en el form: ' + faltan.join(', '));
  form.deleteAllResponses(); // borra los votos de prueba
  Logger.log('Opciones cargadas. Link para votar: ' + form.getPublishedUrl());
}
