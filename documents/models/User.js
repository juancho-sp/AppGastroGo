//Definicion del modelo de usuario

const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
  nombre: { type: String, required: true },
  apellido: { type: String, required: true },
  tipo_documento: { type: String, required: true, enum: ["CC", "TI", "CE", "PA"] },
  documento: { type: String, required: true, unique: true },
  fecha_de_nacimiento: { type: Date, required: true },
  password: { type: String, required: true },
  rol: { type: String, enum: ["admin", "user"], default: "user" },
});

module.exports = mongoose.model("User", userSchema);
