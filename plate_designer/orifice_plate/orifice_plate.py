#!/usr/bin/env python

# Importa bibliotecas necessárias
import math
import numpy as np

class OrificePlate:
    """
    Classe que representa uma placa orificadora.

    Atributos:
        pipe_diameter (float): Diâmetro do tubo.
        orifice_diameter (float): Diâmetro do orifício.
        differential_pressure (float): Pressão diferencial.
        fluid_density (float): Densidade do fluido.
        fluid_viscosity (float): Viscosidade do fluido.
        Reynolds (float): Número de Reynolds.
        edge_type (str): Tipo de borda (padrão "Bordo reto").
        tap_type (str): Tipo de tap (padrão "Tap de canto").
        downstream_pressure_tap_location (float): Posição do tap na pressão abaixo (padrão 0.0).
        upstream_pressure_tap_location (float): Posição do tap na pressão acima (padrão 0.0).

    Métodos:
        orifice_area: Retorna a área do orifício.
        diameter_ratio: Retorna a relação entre o diâmetro do orifício e o diâmetro do tubo.
        orifice_coefficient: Retorna o coeficiente do orifício.
        tap_coefficient: Determina a posição dos taps na pressão acima e abaixo.
        pipe_flow_rate: Retorna a vazão no tubo.
        pipe_velocity: Retorna a velocidade no tubo.
    """
    def __init__(
        self,
        pipe_diameter,
        orifice_diameter,
        differential_pressure,
        fluid_density,
        fluid_viscosity,
        Reynolds,
        edge_type="Bordo reto",
        tap_type="Tap de canto") -> None:
        """
        Construtor da classe OrificePlate.

        Args:
            pipe_diameter (float): Diâmetro do tubo.
            orifice_diameter (float): Diâmetro do orifício.
            differential_pressure (float): Pressão diferencial.
            fluid_density (float): Densidade do fluido.
            fluid_viscosity (float): Viscosidade do fluido.
            Reynolds (float): Número de Reynolds.
            edge_type (str): Tipo de borda (padrão "Bordo reto").
            tap_type (str): Tipo de tap (padrão "Tap de canto").
        """
        self.pipe_diameter = pipe_diameter
        self.orifice_diameter = orifice_diameter
        self.differential_pressure = differential_pressure
        self.fluid_density = fluid_density
        self.fluid_viscosity = fluid_viscosity
        self.Reynolds = Reynolds
        self.edge_type = edge_type
        self.tap_type = tap_type
        self.downstream_pressure_tap_location = 0.0
        self.upstream_pressure_tap_location = 0.0
        
    def orifice_area(self) -> float :
        """
        Calcula a área de um orifício.
        
        Returns
        -------
        float
            A área do orifício.
        """
        return (self.orifice_diameter / 2)**2 * np.pi
    
    def diameter_ratio(self) -> float :
        """
        Calcula a relação entre o diâmetro do orifício e o diâmetro do tubo.
        
        Returns
        -------
        float
            A relação entre o diâmetro do orifício e o diâmetro do tubo.
        """
        return self.orifice_diameter / self.pipe_diameter
    
    def orifice_coefficient(self) -> (float | None):
        """
        Calcula o coeficiente de orifício, considerando os tipos de bordas e tipos de toques.
        
        Returns
        -------
        None
            O coeficiente de orifício.
        """
        self.tap_coefficient()
        beta = self.diameter_ratio()
        L1 = self.upstream_pressure_tap_location
        L2 = self.downstream_pressure_tap_location
        
        if self.edge_type == "Bordo reto":
            Cd = 0.5959 + 0.0312 * beta**2.1 - 0.1840 * beta**8 + 0.0029 * beta**2.5 * (10**6 / self.Reynolds)**0.75 + 0.0900 * (L1/self.pipe_diameter) * (beta**4 / (1 - beta**4)) - 0.0337 * (L2/self.pipe_diameter) * beta**3
        elif self.edge_type == "Bordo redondo":
            Cd = 0.5959 + 0.0312 * beta**2.1 - 0.1840 * beta**8 + 0.0029 * beta**2.5 * (10**6 / self.Reynolds)**0.75 + 0.0900 * (L1/self.pipe_diameter) * (beta**4 / (1 - beta**4)) - 0.0337 * (L2/self.pipe_diameter) * beta**3 + 0.0005 * (1.5 * beta / (1 - beta))**2
        elif self.edge_type == "Bordo em V":
            Cd = 0.5959 + 0.0312 * beta**2.1 - 0.1840 * beta**8 + 0.0029 * beta**2.5 * (10**6 / self.Reynolds)**0.75 + 0.0900 * (L1/self.pipe_diameter) * (beta**4 / (1 - beta**4)) - 0.0337 * (L2/self.pipe_diameter) * beta**3 + 0.0005 * (2.5 * beta / (1 - beta))**2
        else:
            return None
        return Cd

    def tap_coefficient(self) -> None :
        """
        Este método calcula e define a localização do ponto de medida de pressão com base no tipo de ponto de medida.
        
        Returns
        -------
        None
            O coeficiente de tap.
        """
        if self.tap_type == "Tap central":
            self.upstream_pressure_tap_location = 0.0254
            self.downstream_pressure_tap_location = 0.0254
        elif self.tap_type == "Tap de canto":
            self.upstream_pressure_tap_location = 0.0
            self.downstream_pressure_tap_location = 0.0
        elif self.tap_type == "Tap de tubo":
            self.upstream_pressure_tap_location = self.pipe_diameter * 2.5
            self.downstream_pressure_tap_location = self.pipe_diameter * 8
        elif self.tap_type == "Tap radial":
            self.upstream_pressure_tap_location = self.pipe_diameter
            self.downstream_pressure_tap_location = self.pipe_diameter / 2

    def pipe_flow_rate(self) -> float :
        """
        Este método calcula a vazão de escoamento na tubulação usando o coeficiente de orifício, 
        a pressão diferencial, a densidade do fluido e a área do orifício.
        
        Returns
        -------
        float
            taxa de vazão.
        """
        return self.orifice_coefficient() * math.sqrt(2 * self.differential_pressure * self.fluid_density) * self.orifice_area()
    
    def pipe_flow_rate(self, input_pressure) -> float :
        """
        Este método calcula a vazão de escoamento na tubulação usando o coeficiente de orifício,
        a pressão diferencial, a densidade do fluido e a área do orifício.
        
        Returns
        -------
        float
            taxa de vazão.
        """
        return self.orifice_coefficient() * math.sqrt(2 * input_pressure * self.fluid_density) * self.orifice_area()