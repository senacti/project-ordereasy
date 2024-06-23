<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a newly created user in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $request->validate([
            'tipoIdentificacion' => 'required|string|max:255',
            'identificacion' => 'required|string|max:255|unique:users,identificacion',
            'primerNombre' => 'required|string|max:255',
            'primerApellido' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users,email',
            'password' => 'required|string|min:8|confirmed',
            'codigoUsuario' => 'nullable|string|max:255',
        ]);

        $user = User::create([
            'tipoIdentificacion' => $request->tipoIdentificacion,
            'identificacion' => $request->identificacion,
            'primerNombre' => $request->primerNombre,
            'primerApellido' => $request->primerApellido,
            'email' => $request->email,
            'password' => bcrypt($request->password),
            'codigoUsuario' => $request->codigoUsuario ?? 'uno',
        ]);

        return redirect()->route('users.index')->with('success', 'Usuario creado correctamente');
    }
}
