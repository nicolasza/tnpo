
class modelTnpo:
    """Modelo de clase para cargar y ejecutar modelos de PyTorch"""


    
    def __init__(self, model_name, model_type, model_path):
        """Clase para manejar la carga y ejecución de modelos de PyTorch.
        Atributos:
            model_name (str): Nombre del modelo.
            model_type (str): Tipo de modelo (ej. "torchscript").
            model_path (str): Ruta al archivo del modelo.
            model: Instancia del modelo cargado.
        """
        self.model_name = model_name
        self.model_type = model_type
        self.model_path = model_path

    def es_lista_de_enteros(self,arr):
        """Verifica si una lista contiene solo enteros.
        Args:
            arr (list): Lista a verificar.
        
        Returns:
            bool: True si todos los elementos son enteros, False en caso contrario.
        """
        return all(isinstance(x, int) for x in arr)

    
    def load_model(self):
        """Carga el modelo de PyTorch desde la ruta especificada.
        Args:
            None
        
        Returns:
            model: Modelo cargado.
        
        Raises:
            Exception: Si ocurre un error al cargar el modelo.
        """
        import torch
        try:
            self.model = torch.jit.load(self.model_path)
            self.model.eval()
            print(f"Modelo {self.model_name} cargado correctamente desde {self.model_path}")
        except Exception as e:
            print(f"Error al cargar el modelo {self.model_name}: {e}")
            self.model = None
            raise e
        return self.model
    
    
    def infer(self, input):
        """Realiza la inferencia con el modelo cargado.
        Args:
            input (list): Lista de enteros para la inferencia.
        
        Returns:
            output_tensor: Tensor de salida del modelo.
        
        Raises:
            ValueError: Si el modelo no está cargado o si el input no es una lista de enteros.
            Exception: Si ocurre un error durante la inferencia.
        """
        import torch
        if self.model is None:
            raise ValueError("Modelo no cargado. Por favor, carga el modelo antes de inferir.")
        if not self.es_lista_de_enteros(input):
            raise ValueError("El input debe ser una lista de enteros.")
        try:
            input_tensor=torch.tensor(input)
            output_tensor = self.model(input_tensor)
            return output_tensor
        except Exception as e:
            raise e
