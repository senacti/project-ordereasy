@extends('layouts.app')
@section('content')
<div class="container">
 
<div class="container">
    @if(Session::has('mensaje'))
    <div class="alert alert-success alert-dismissible fade show" role="alert">
        {{ Session::get('mensaje') }}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    @endif


<br>
<a href="{{url('empleado/create')}}" class="btn btn-success"> Registrar nuevo empleado</a>
<br>
<table class="table table-dark">

    <thead class="thead-dark">
        <tr>
            <th>#</th>
            <th>Foto</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Correo</th>
            <th>Direccion</th>
            <th>Acciones</th>
        </tr>
    </thead>

    <tbody> 
        @foreach($empleados as $empleado)
        <tr>
            <td>{{$empleado->id }}</td>
            <td>
                <img src="{{asset('storage').'/'.$empleado->Foto}}" width="100" height="100"  alt="">
            </td>
            <td>{{$empleado->Nombre }}</td>
            <td>{{$empleado->Apellido }}</td>
            <td>{{$empleado->Correo }}</td>
            <td>{{$empleado->Direccion }}</td>
            <td>
                <a href="{{url('/empleado/'.$empleado->id.'/edit')}}" class="btn btn-warning">
                Editar
                </a>
            
            
                <form action="{{url('/empleado/'.$empleado->id)}}" method="post" class="d-inline" >
                    @csrf
                    {{method_field('DELETE')}}
                    <input type="submit" class="btn btn-danger" onclick="return confirm('Esta seguro?')" 
                    value="Borrar">
                </form>
            </td>
        </tr>
        @endforeach
    </tbody>
</table>
{!!$empleados->Links()!!}
</div>
@endsection