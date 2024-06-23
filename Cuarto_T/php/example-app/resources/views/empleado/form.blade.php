<h1>{{$modo}} Empleado</h1>

@if(count($errors)>0)
<div class="alert alert-danger" role="alert">
    <ul>
@foreach($errors->all() as $error)
<li>{{$error}}</li>
@endforeach
</ul>
</div>

@endif




<div class="form-group">
<label for="Nombre">Primer Nombre</label>
<input type="text" class="form-control" name="Nombre" value="{{isset($empleado->Nombre)?$empleado->Nombre:old('Nombre') }}" id="Nombre">
<br></div>

<div class="form-group">
<label for="Apellido">Primer Apellido </label>
<input type="text" class="form-control" name="Apellido" value="{{isset($empleado->Apellido)?$empleado->Apellido:old('Apellido')}}" id="Apellido">
<br></div>


<div class="form-group">
<label for="Correo">Correo </label>
<input type="text"  class="form-control" name="Correo" value="{{isset($empleado->Correo)?$empleado->Correo:old('Correo')}}" id="Correo">
<br></div>

<div class="form-group">
<label for="Apellido">Direccion </label>
<input type="text" class="form-control" name="Direccion" value="{{isset($empleado->Direccion)?$empleado->Direccion:old('Direccion')}}" id="Direccion">
<br></div>


<label for="Foto"> </label>
@if(isset($empleado->Foto))
<img src="{{asset('storage').'/'.$empleado->Foto}}" width="100" height="100"  alt=""><br>
@endif
<br>
<input class="form-control" type="file" name="Foto"  value="" id="Foto">
<br>
<br>
<br>
<input type="submit" class="btn btn-success"  value="{{$modo}} Datos">
<a href="{{url('empleado/')}}"  class="btn btn-warning"> Regresar</a>