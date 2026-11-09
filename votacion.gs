// Votación de "Te canto las 40". Se usa en script.google.com (Apps Script).
// 1) Ahora: ejecutar crearFormulario. Crea el form con opciones de prueba y muestra los links.
// 2) Después del karaoke: reemplazar OPCIONES con los nombres reales y ejecutar cargarOpciones.

const TITULO = 'Te canto las 40: votación';

const OPCIONES = {
  'Mejor cantante': ['Opción 1', 'Opción 2', 'Opción 3'],
  'Mejor show': ['Opción 1', 'Opción 2', 'Opción 3'],
  'Mejor personificación': ['Opción 1', 'Opción 2', 'Opción 3'],
  'Mejor dúo o grupo': ['Opción 1', 'Opción 2', 'Opción 3'],
  'Mejor coreografía': ['Opción 1', 'Opción 2', 'Opción 3'],
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
