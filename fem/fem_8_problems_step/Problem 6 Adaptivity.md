
We can introduce adaptivity into MOOSE, by adding markers
https://mooseframework.inl.gov/getting_started/examples_and_tutorials/examples/ex05_amr.html
```
[Adaptivity]
  marker = errorfrac # this specifies which marker from 'Markers' subsection to use
  steps = 2 # run adaptivity 2 times, recomputing solution, indicators, and markers each time

  # Use an indicator to compute an error-estimate for each element:
  [./Indicators]
    # create an indicator computing an error metric for the convected variable
    [./error]
      # arbitrary, use-chosen name
      type = GradientJumpIndicator
      variable = convected
      outputs = none
    [../]
  [../]

  # Create a marker that determines which elements to refine/coarsen based on error estimates
  # from an indicator:
  [./Markers]
    [./errorfrac]
      # arbitrary, use-chosen name (must match 'marker=...' name above
      type = ErrorFractionMarker
      indicator = error # use the 'error' indicator specified above
      refine = 0.5 # split/refine elements in the upper half of the indicator error range
      coarsen = 0 # don't do any coarsening
      outputs = none
    [../]
  [../]
[]
```
