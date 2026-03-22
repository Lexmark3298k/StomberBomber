<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <Configuration Condition=" '$(Configuration)' == '' ">Debug</Configuration>
    <SchemaVersion>2.0</SchemaVersion>
    <ProjectGuid>{A1B2C3D4-E5F6-7890-AB12-CD34EF567890}</ProjectGuid>
    <ProjectHome>.</ProjectHome>
    <StartupFile>main.py</StartupFile>
    <SearchPath>.</SearchPath>
    <WorkingDirectory>.</WorkingDirectory>
    <OutputPath>.</OutputPath>
    <Name>StomberBomber</Name>
    <RootNamespace>StomberBomber</RootNamespace>
    <InterpreterId>Global|PythonCore|3.9</InterpreterId>
  </PropertyGroup>
  <PropertyGroup Condition=" '$(Configuration)' == 'Debug' ">
    <DebugSymbols>true</DebugSymbols>
    <EnableUnmanagedDebugging>false</EnableUnmanagedDebugging>
  </PropertyGroup>
  <ItemGroup>
    <Compile Include="main.py" />
    <Compile Include="settings.py" />
    <Compile Include="game_state.py" />
    <Compile Include="levels\__init__.py" />
    <Compile Include="levels\level_base.py" />
    <Compile Include="levels\salon1.py" />
    <Compile Include="levels\salon2.py" />
    <Compile Include="levels\salon3.py" />
    <Compile Include="levels\salon4.py" />
    <Compile Include="levels\salon5.py" />
    <Compile Include="classes\__init__.py" />
    <Compile Include="classes\player.py" />
    <Compile Include="classes\enemies.py" />
    <Compile Include="classes\lasers.py" />
    <Compile Include="classes\button.py" />
    <Compile Include="classes\hiding_spot.py" />
    <Compile Include="classes\tv_puzzle.py" />
    <Compile Include="classes\effects.py" />
  </ItemGroup>
  <ItemGroup>
    <Content Include="assets\fonts\press_start.ttf" />
    <Content Include="assets\sounds\*.wav" />
    <Content Include="assets\sprites\*.png" />
  </ItemGroup>
</Project>