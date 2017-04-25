#script 

# Import arcpy module
import arcpy

#Step 1: sample raster
This tool takes a raster dataset, resamples it to a use defined resolution and  creates a point file
where the points are the centroids of the raster cells. Point values represent the value of the underlying 
raster grid cell. 

# Script arguments
Avkat_DBO_dem_quickbird_extent = arcpy.GetParameterAsText(0)
if Avkat_DBO_dem_quickbird_extent == '#' or not Avkat_DBO_dem_quickbird_extent:
    Avkat_DBO_dem_quickbird_extent = "Database Connections\\Connection to geodata.cofc.edu.sde\\AVKAT.DBO.DEM_QUICKBIRD_EXTENT" # provide a default value if unspecified

Output_Cell_Size = arcpy.GetParameterAsText(1)
if Output_Cell_Size == '#' or not Output_Cell_Size:
    Output_Cell_Size = "500 500" # provide a default value if unspecified

viewshed_sample_points = arcpy.GetParameterAsText(2)
if viewshed_sample_points == '#' or not viewshed_sample_points:
    viewshed_sample_points = "C:\\datatemp\\datatemp.gdb\\viewshed_sample_points" # provide a default value if unspecified

# Local variables:
avkat_dem = "C:\\datatemp\\datatemp.gdb\\avkat_dem"
avkat_dem_resampled4viewshed_sample = "C:\\datatemp\\datatemp.gdb\\avkat_dem_resampled4viewshed_sample"
viewshed_sample_points__2_ = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\viewshed_sample_points"

# Process: Resample
arcpy.Resample_management(avkat_dem, avkat_dem_resampled4viewshed_sample, Output_Cell_Size, "NEAREST")

# Process: Raster to Point
arcpy.RasterToPoint_conversion(avkat_dem_resampled4viewshed_sample, viewshed_sample_points, "Value")

# Process: Copy Features
arcpy.CopyFeatures_management(viewshed_sample_points, viewshed_sample_points__2_, "", "0", "0", "0")

#Step 2: viewshed for sampled points
Iterates through 1330 points to create a shankload of view sheds. 

# Load required toolboxes
#arcpy.ImportToolbox("Model Functions")

# Script arguments
gdbtemp = arcpy.GetParameterAsText(0)
if gdbtemp == '#' or not gdbtemp:
    gdbtemp = "C:\\datatemp\\cum_viewshed.gdb" # provide a default value if unspecified

# Local variables:
avkat_dem = "C:\\datatemp\\datatemp.gdb\\avkat_dem"
viewshed_sample_points = "C:\\datatemp\\datatemp.gdb\\viewshed_sample_points"
I_sample_points = viewshed_sample_points
viewshed_value_ = "C:\\datatemp\\cum_viewshed.gdb\\viewshed%value%"
Value = "1330"
Output_above_ground_level_raster = ""

# Process: Iterate Feature Selection
arcpy.IterateFeatureSelection_mb(viewshed_sample_points, "", "false")

# Process: Viewshed
arcpy.gp.Viewshed_sa(avkat_dem, I_sample_points, viewshed_value_, "1", "CURVED_EARTH", "0.13", Output_above_ground_level_raster)

#Step 3: viewshedadder
Iterative function where we take all the view sheds and add them together. All feature viewsheds are being added
into one cumulative viewshed file.

# Load required toolboxes
arcpy.ImportToolbox("Model Functions")

# Script arguments
cum_viewshed_gdb = arcpy.GetParameterAsText(0)
if cum_viewshed_gdb == '#' or not cum_viewshed_gdb:
    cum_viewshed_gdb = "C:\\datatemp\\cum_viewshed.gdb" # provide a default value if unspecified

cum_viewshed_final = arcpy.GetParameterAsText(1)
if cum_viewshed_final == '#' or not cum_viewshed_final:
    cum_viewshed_final = "c:\\\\datatemp\\cum_viewshed.gdb\\cum_viewshed_final" # provide a default value if unspecified

# Local variables:
Name = "cum_viewshed_final"
viewshed1 = "C:\\datatemp\\cum_viewshed.gdb\\cum_viewshed_final"
cum_viewshed_final__2_ = "C:\\datatemp\\cum_viewshed.gdb\\cum_viewshed_final"
Plus_Raster1 = "C:\\datatemp\\cum_viewshed.gdb\\Plus_Raster1"
Delete_succeeded = "true"

# Process: Iterate Rasters
arcpy.IterateRasters_mb(cum_viewshed_gdb, "", "", "NOT_RECURSIVE")

# Process: Plus
arcpy.gp.Plus_sa(viewshed1, cum_viewshed_final__2_, Plus_Raster1)

# Process: Delete
arcpy.Delete_management(cum_viewshed_final__2_, "RasterDataset")

# Process: Copy
arcpy.Copy_management(Plus_Raster1, cum_viewshed_final, "RasterDataset")

#Step 4: get OPs for sites 

# Script arguments
site_layer = arcpy.GetParameterAsText(0)
if site_layer == '#' or not site_layer:
    site_layer = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\sites_morans_Ar_Merge" # provide a default value if unspecified

# Local variables:
Avkat_DBO_ops = "Database Connections\\avkat_current geospatial.sde\\Avkat.DBO.features_sus_ops\\Avkat.DBO.ops"
site_points = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\site_points"

# Process: Spatial Join
arcpy.SpatialJoin_analysis(Avkat_DBO_ops, site_layer, site_points, "JOIN_ONE_TO_MANY", "KEEP_ALL", "Id \"Id\" true true false 4 Long 0 10 ,First,#,Database Connections\\Connection to geodata.cofc.edu.sde\\Avkat.DBO.features_sus_ops\\Avkat.DBO.ops,Id,-1,-1;OP \"OP\" true true false 10 Text 0 0 ,First,#,Database Connections\\Connection to geodata.cofc.edu.sde\\Avkat.DBO.features_sus_ops\\Avkat.DBO.ops,OP,-1,-1;SU \"SU\" true true false 50 Text 0 0 ,First,#,Database Connections\\Connection to geodata.cofc.edu.sde\\Avkat.DBO.features_sus_ops\\Avkat.DBO.ops,SU,-1,-1;feature_no \"feature_no\" true true false 50 Text 0 0 ,First,#,O:\\cross_regional\\data\\databases\\functional_model.gdb\\sites_mbz_morans_Ar,feature_no,-1,-1", "INTERSECT", "", "")

#Step 5: Taking observation points for given sites and running a viewshed from those points. Adding results of the viewshed to the attribute table. 

# Load required toolboxes
arcpy.ImportToolbox("Model Functions")

# Script arguments
AVKAT_DBO_DEM_QUICKBIRD_EXTENT = arcpy.GetParameterAsText(0)
if AVKAT_DBO_DEM_QUICKBIRD_EXTENT == '#' or not AVKAT_DBO_DEM_QUICKBIRD_EXTENT:
    AVKAT_DBO_DEM_QUICKBIRD_EXTENT = "Database Connections\\Connection to geodata.cofc.edu.sde\\AVKAT.DBO.DEM_QUICKBIRD_EXTENT" # provide a default value if unspecified

cumvisibility_gdb = arcpy.GetParameterAsText(1)
if cumvisibility_gdb == '#' or not cumvisibility_gdb:
    cumvisibility_gdb = "C:\\datatemp\\cumvisibility.gdb" # provide a default value if unspecified

site_points = arcpy.GetParameterAsText(2)
if site_points == '#' or not site_points:
    site_points = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\site_points" # provide a default value if unspecified

# Local variables:
I_site_visibility_points_feature_no = site_points
Value = "4122"
f_value_ = "C:\\datatemp\\cumvisibility.gdb\\f%value%"
f_value___3_ = f_value_
f_value___2_ = f_value___3_

# Process: Iterate Feature Selection
arcpy.IterateFeatureSelection_mb(site_points, "feature_no #", "false")

# Process: Viewshed
arcpy.gp.Viewshed_sa(AVKAT_DBO_DEM_QUICKBIRD_EXTENT, I_site_visibility_points_feature_no, f_value_, "1", "FLAT_EARTH", "0.13", "")

# Process: Add Field
arcpy.AddField_management(f_value_, "visibility_pct", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field
arcpy.CalculateField_management(f_value___3_, "visibility_pct", "[COUNT] /368636", "VB", "")

#Step 6: Taking the input (sample points across the entire region), ran a viewshed, taking results and adding it to the attribute table of the sample points (input)
# Load required toolboxes
arcpy.ImportToolbox("Model Functions")

# Script arguments
Input_site_locations = arcpy.GetParameterAsText(0)
if Input_site_locations == '#' or not Input_site_locations:
    Input_site_locations = "C:\\datatemp\\datatemp.gdb\\viewshed_sample_points" # provide a default value if unspecified

# Local variables:
I_sample_points1_pointid = Input_site_locations
Value = "1330"
I_sample_points_pointid__2_ = I_sample_points1_pointid
viewshed_value_ = "C:\\datatemp\\cum_viewshed.gdb\\viewshed%value%"
datatemp_gdb = "C:\\datatemp\\datatemp.gdb"
point = "C:\\datatemp\\datatemp.gdb\\point"
viewnumber = point
sites1_gdb = "C:\\datatemp\\sites1.gdb"

# Process: Iterate Feature Selection
arcpy.IterateFeatureSelection_mb(Input_site_locations, "pointid #", "false")

# Process: Table to Table
arcpy.TableToTable_conversion(viewshed_value_, datatemp_gdb, "point", "\"Value\" = 1", "Value \"Value\" false true false 4 Long 0 0 ,First,#,C:\\datatemp\\cum_viewshed.gdb\\viewshed%value%\\Band_1,Value,-1,-1;Count \"Count\" false true false 8 Double 0 0 ,First,#,C:\\datatemp\\cum_viewshed.gdb\\viewshed%value%\\Band_1,Count,-1,-1", "")

# Process: Get Field Value
arcpy.GetFieldValue_mb(point, "COUNT", "Long", "0")

# Process: Calculate Field (2)
arcpy.CalculateField_management(I_sample_points1_pointid, "visible", "%viewnumber%", "PYTHON_9.3", "")

#Step 7:Taking the observation points, creates a buffer where then the clip function removes the remaining raster (naismith_cost). Returns cost distance function (value)
# Load required toolboxes
arcpy.ImportToolbox("Model Functions")

# Script arguments
cumcost_gdb = arcpy.GetParameterAsText(0)
if cumcost_gdb == '#' or not cumcost_gdb:
    cumcost_gdb = "C:\\datatemp\\cumcost.gdb" # provide a default value if unspecified

site_points = arcpy.GetParameterAsText(1)
if site_points == '#' or not site_points:
    site_points = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\site_points" # provide a default value if unspecified

# Local variables:
I_site_points_feature_no = site_points
Value = "1"
naismith_cost__2_ = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\naismith_cost"
site_points_Buffer = "C:\\datatemp\\cumcost.gdb\\site_points_Buffer"
naismith_cost_Clip = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\naismith_cost_Clip"
f_value_ = "C:\\datatemp\\cumcost.gdb\\f%value%"
Output_backlink_raster = ""

# Set Geoprocessing environments
arcpy.env.extent = "683832.453472731 4483716.55816339 701442.453472731 4502556.55816339"

# Process: Iterate Feature Selection
arcpy.IterateFeatureSelection_mb(site_points, "feature_no #", "false")

# Process: Buffer
arcpy.Buffer_analysis(I_site_points_feature_no, site_points_Buffer, "500 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")

# Process: Clip
arcpy.Clip_management(naismith_cost__2_, "689408.5928 4489877.9461 694393.5022 4495825.9547", naismith_cost_Clip, site_points_Buffer, "-3.402823e+038", "NONE", "NO_MAINTAIN_EXTENT")

# Process: Cost Distance
arcpy.gp.CostDistance_sa(I_site_points_feature_no, naismith_cost_Clip, f_value_, "", Output_backlink_raster, "", "", "", "")


#Step 8: 
# Load required toolboxes
arcpy.ImportToolbox("Model Functions")


# Local variables:
sites_morans_Ar_Merge = "sites_morans_Ar_Merge"
sites_morans_Ar_Merge__3_ = sites_morans_Ar_Merge
sites_morans_Ar_Merge__4_ = sites_morans_Ar_Merge__3_
sites_morans_Ar_Merge__5_ = sites_morans_Ar_Merge__4_
cumcost_gdb = "C:\\datatemp\\cumcost.gdb"
Name = "cost4016"
sites_mbz_morans_Ar__2_ = sites_morans_Ar_Merge__5_
sites_mbz_morans_Ar__7_ = sites_morans_Ar_Merge__5_
cumcost4016 = "C:\\datatemp\\cumcost.gdb\\cost4016"
Property_type = "MEAN"
c_ave = Property_type
Property_type__2_ = "STD"
c_std = Property_type__2_

# Process: Add Field
arcpy.AddField_management(sites_morans_Ar_Merge, "cum_avg", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (2)
arcpy.AddField_management(sites_morans_Ar_Merge__3_, "std", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Iterate Rasters
arcpy.IterateRasters_mb(cumcost_gdb, "cost*", "", "NOT_RECURSIVE")

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management(sites_morans_Ar_Merge__4_, "NEW_SELECTION", "\"feature_no\" = '%Name%'")

# Process: Get Raster Properties
arcpy.GetRasterProperties_management(cumcost4016, Property_type, "")

# Process: Calculate Field (2)
arcpy.CalculateField_management(sites_morans_Ar_Merge__5_, "cum_avg", "%c_ave%", "PYTHON_9.3", "")

# Process: Get Raster Properties (2)
arcpy.GetRasterProperties_management(cumcost4016, Property_type__2_, "")

# Process: Calculate Field (3)
arcpy.CalculateField_management(sites_morans_Ar_Merge__5_, "std", "%c_std%", "PYTHON_9.3", "")

#Step 9: 
# Load required toolboxes
arcpy.ImportToolbox("Model Functions")


# Local variables:
sites_morans_Ar_Merge__3_ = "sites_morans_Ar_Merge"
sites_morans_Ar_Merge__4_ = sites_morans_Ar_Merge__3_
cumcost_gdb = "C:\\datatemp\\cumcost.gdb"
Name = "f5401"
sites_morans_Ar_Merge__2_ = sites_morans_Ar_Merge__4_
sites_morans_Ar_Merge = sites_morans_Ar_Merge__4_
f4016 = "C:\\datatemp\\cumcost.gdb\\f5401"
Property_type = "MEAN"
c_ave = Property_type
Property_type__2_ = "STD"
c_std = Property_type__2_
sample_points = "C:\\datatemp\\datatemp.gdb\\sample_points"

# Process: Iterate Rasters
arcpy.IterateRasters_mb(cumcost_gdb, "f*", "", "NOT_RECURSIVE")

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management(sites_morans_Ar_Merge__3_, "NEW_SELECTION", "\"feature_no\" = '%Name%'")

# Process: Get Raster Properties
arcpy.GetRasterProperties_management(f4016, Property_type, "")

# Process: Calculate Field (2)
arcpy.CalculateField_management(sites_morans_Ar_Merge__4_, "cumcost_avg", "%c_ave%", "PYTHON_9.3", "")

# Process: Get Raster Properties (2)
arcpy.GetRasterProperties_management(f4016, Property_type__2_, "")

# Process: Calculate Field (3)
arcpy.CalculateField_management(sites_morans_Ar_Merge__4_, "cumcost_stdev", "%c_std%", "PYTHON_9.3", "")

#step 10: 

# Load required toolboxes
arcpy.ImportToolbox("Model Functions")

# Script arguments
location_of_site_viewshed_files = arcpy.GetParameterAsText(0)
if location_of_site_viewshed_files == '#' or not location_of_site_viewshed_files:
    location_of_site_viewshed_files = "C:\\datatemp\\cumvisibility.gdb" # provide a default value if unspecified

# Local variables:
Property_type = "MAXIMUM"
not_seen = Property_type
sites_morans_Ar_Merge__5_ = ""
sites_morans_Ar_Merge__4_ = sites_morans_Ar_Merge__5_
sites_morans_Ar_Merge__2_ = "sites_morans_Ar_Merge"
sites_morans_Ar_Merge__3_ = sites_morans_Ar_Merge__2_
Name = "f4107"
sites_morans_Ar_Merge = sites_morans_Ar_Merge__3_
cumcost4016 = "C:\\datatemp\\cumvisibility.gdb\\f4107"
f4016_TableSelect = "D:\\Users\\newhardj\\Documents\\ArcGIS\\Default.gdb\\f4016_TableSelect"
Value = f4016_TableSelect
sites_morans_Ar_Merge__6_ = sites_morans_Ar_Merge
N_of_cells_in_raster = "368636"
Divide_f40165 = ""

# Process: Get Raster Properties
arcpy.GetRasterProperties_management("", Property_type, "")

# Process: Add Field
arcpy.AddField_management("", "viewable_pct", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (2)
arcpy.AddField_management(sites_morans_Ar_Merge__5_, "not_viewable_pct", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Iterate Rasters
arcpy.IterateRasters_mb(location_of_site_viewshed_files, "f*", "", "NOT_RECURSIVE")

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management(sites_morans_Ar_Merge__2_, "NEW_SELECTION", "\"feature_no\" = '%Name%'")

# Process: Table Select
arcpy.TableSelect_analysis(cumcost4016, f4016_TableSelect, "")

# Process: Get Field Value
arcpy.GetFieldValue_mb(f4016_TableSelect, "visibility_pct", "String", "0")

# Process: Calculate Field (2)
arcpy.CalculateField_management(sites_morans_Ar_Merge__3_, "not_viewable_pct", Value, "PYTHON_9.3", "")

# Process: Calculate Field (3)
arcpy.CalculateField_management(sites_morans_Ar_Merge, "viewable_pct", "1- [not_viewable_pct]", "VB", "")

# Process: Divide
arcpy.gp.Divide_sa("", N_of_cells_in_raster, Divide_f40165)

#step 11:
# Import arcpy module
import arcpy


# Local variables:
AVKAT_DBO_DEM_QUICKBIRD_EXTENT = "Database Connections\\Connection to geodata.cofc.edu.sde\\AVKAT.DBO.DEM_QUICKBIRD_EXTENT"
aoi_dem = "D:\\Users\\newhardj\\Documents\\ArcGIS\\Default.gdb\\aoi_dem"
Property = ""
Input_raster_or_constant_value_2 = "1"
avkat = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\avkat"
slope_dem = "D:\\Users\\newhardj\\Documents\\ArcGIS\\Default.gdb\\slope_dem"
v5__2_ = "5"
Greater_slop2 = "D:\\Users\\newhardj\\Documents\\ArcGIS\\Default.gdb\\Greater_slop1"
v12__2_ = "12"
LessThan12__2_ = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\LessThan12"
mor5less12slp__3_ = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\mor5less12slp"
v1_998__2_ = "1.998"
v5to12_penalty = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\ms5to12"
PI__2_ = "3.141592654"
dem_x_pi = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\dem_x_pi"
v180__2_ = "180"
demxpi_by_180 = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\demxpi_by_180"
Tan_demxpi_b1 = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\Tan_demxpi_b1"
v21_58828612__2_ = "21.58828612"
rise_of_all_aoi__2_ = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\rise_of_aoi"
nais_penalties_5to12 = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\nais_penalties_5to12"
v6__2_ = "6"
Greaterthan_12 = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\Greaterthan_12"
ms_more12__3_ = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\ms_more12"
nais_penalties_more12 = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\nais_penalties_more12"
naismith_rule = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\naismith_cost"
Output_backlink_raster__2_ = ""
d2town_sec = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\d2town_sec"
v3600__2_ = "1200"
d2town = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\d2town"
stream = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\stream"
Output_backlink_raster = ""
d2h2o_sec = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\d2h2o_sec"
v1200 = "1200"
d2water_min = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\d2water_min"
v60 = "60"
d2water = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\d2water"

# Process: Copy Raster
arcpy.CopyRaster_management(AVKAT_DBO_DEM_QUICKBIRD_EXTENT, aoi_dem, "", "", "65536", "NONE", "NONE", "", "NONE", "NONE", "", "NONE")

# Process: Get Raster Properties
arcpy.GetRasterProperties_management(aoi_dem, "CELLSIZEX", "")

# Process: Slope (2)
arcpy.gp.Slope_sa(aoi_dem, slope_dem, "DEGREE", "1")

# Process: Greater Than Equal (4)
arcpy.gp.GreaterThanEqual_sa(slope_dem, v5__2_, Greater_slop2)

# Process: Less Than (3)
arcpy.gp.LessThan_sa(slope_dem, v12__2_, LessThan12__2_)

# Process: Times (3)
arcpy.gp.Times_sa(Greater_slop2, LessThan12__2_, mor5less12slp__3_)

# Process: Times (11)
arcpy.gp.Times_sa(mor5less12slp__3_, v1_998__2_, v5to12_penalty)

# Process: Times (14)
arcpy.gp.Times_sa(slope_dem, PI__2_, dem_x_pi)

# Process: Divide (4)
arcpy.gp.Divide_sa(dem_x_pi, v180__2_, demxpi_by_180)

# Process: Tan (2)
arcpy.gp.Tan_sa(demxpi_by_180, Tan_demxpi_b1)

# Process: Times (8)
arcpy.gp.Times_sa(Tan_demxpi_b1, v21_58828612__2_, rise_of_all_aoi__2_)

# Process: Times (9)
arcpy.gp.Times_sa(v5to12_penalty, rise_of_all_aoi__2_, nais_penalties_5to12)

# Process: Greater Than Equal (3)
arcpy.gp.GreaterThanEqual_sa(slope_dem, v12__2_, Greaterthan_12)

# Process: Times (13)
arcpy.gp.Times_sa(v6__2_, Greaterthan_12, ms_more12__3_)

# Process: Times (6)
arcpy.gp.Times_sa(rise_of_all_aoi__2_, ms_more12__3_, nais_penalties_more12)

# Process: sums all penalties for naismith's rule
arcpy.gp.RasterCalculator_sa("\"%nais_penalties_5to12%\" + \"%nais_penalties_more12%\" + 15.12", naismith_rule)

# Process: Cost Distance (2)
arcpy.gp.CostDistance_sa(avkat, naismith_rule, d2town_sec, "", Output_backlink_raster__2_, "", "", "", "")

# Process: Divide (2)
arcpy.gp.Divide_sa(d2town_sec, v3600__2_, d2town)

# Process: Cost Distance
arcpy.gp.CostDistance_sa(stream, naismith_rule, d2h2o_sec, "", Output_backlink_raster, "", "", "", "")

# Process: Divide
arcpy.gp.Divide_sa(d2h2o_sec, v1200, d2water_min)

# Process: Divide (3)
arcpy.gp.Divide_sa(d2water_min, v60, d2water)

#step 12:

# Import arcpy module
import arcpy

# Load required toolboxes
arcpy.ImportToolbox("Model Functions")


# Local variables:
site_points = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\site_points"
site_points__2_ = site_points
datatemp = "C:\\datatemp"
d2h2o_gdb = datatemp
d2avkat_gdb = datatemp
site_points__7_ = site_points__2_
d2water = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\d2water"
d2h2o_sitepoints = "D:\\Users\\newhardj\\Documents\\ArcGIS\\Default.gdb\\d2h2o_sitepoints"
d2h2o_sitepoints__2_ = d2h2o_sitepoints
d2h2o_sitepoints__4_ = d2h2o_sitepoints__2_
d2_avkat = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\d2_avkat"
d2h2od2avkat_sitepoints = "D:\\Users\\newhardj\\Documents\\ArcGIS\\Default.gdb\\d2h2od2avkat_sitepoints"
d2h2od2avkat_sitepoints__4_ = d2h2od2avkat_sitepoints
d2h2od2avkat_sitepoints__3_ = d2h2od2avkat_sitepoints__4_
I_d2h2od2avkat_sitepoints_feature_no = d2h2od2avkat_sitepoints__3_
sites_morans_Ar_Merge = "sites_morans_Ar_Merge"
sites_morans_Ar_Merge__2_ = sites_morans_Ar_Merge
sites_morans_Ar_Merge__3_ = sites_morans_Ar_Merge__2_
sites_morans_Ar_Merge__5_ = sites_morans_Ar_Merge__3_
Value = "1"
f_value___3_ = "C:\\datatemp\\d2avkat.gdb\\f%value%"
f_value_ = "C:\\datatemp\\d2h2o.gdb\\f%value%"

# Process: Create File GDB (2)
arcpy.CreateFileGDB_management(datatemp, "d2avkat", "CURRENT")

# Process: Create File GDB
arcpy.CreateFileGDB_management(datatemp, "d2h2o", "CURRENT")

# Process: Add Field
arcpy.AddField_management(site_points, "d2water", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (2)
arcpy.AddField_management(site_points__2_, "d2avkat", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Extract Values to Points
arcpy.gp.ExtractValuesToPoints_sa(site_points__7_, d2water, d2h2o_sitepoints, "NONE", "VALUE_ONLY")

# Process: Calculate Field
arcpy.CalculateField_management(d2h2o_sitepoints, "d2water", "[RASTERVALU]", "VB", "")

# Process: Delete Field
arcpy.DeleteField_management(d2h2o_sitepoints__2_, "RASTERVALU")

# Process: Extract Values to Points (2)
arcpy.gp.ExtractValuesToPoints_sa(d2h2o_sitepoints__4_, d2_avkat, d2h2od2avkat_sitepoints, "NONE", "VALUE_ONLY")

# Process: Calculate Field (2)
arcpy.CalculateField_management(d2h2od2avkat_sitepoints, "d2avkat", "[RASTERVALU]", "VB", "")

# Process: Delete Field (2)
arcpy.DeleteField_management(d2h2od2avkat_sitepoints__4_, "RASTERVALU")

# Process: Add Field (3)
arcpy.AddField_management(sites_morans_Ar_Merge, "d2h2o", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Add Field (4)
arcpy.AddField_management(sites_morans_Ar_Merge__2_, "d2avkat", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Iterate Feature Selection
arcpy.IterateFeatureSelection_mb(d2h2od2avkat_sitepoints__3_, "feature_no #", "false")

# Process: Summary Statistics (2)
arcpy.Statistics_analysis(I_d2h2od2avkat_sitepoints_feature_no, f_value___3_, "d2water MEAN", "")

# Process: Summary Statistics
arcpy.Statistics_analysis(I_d2h2od2avkat_sitepoints_feature_no, f_value_, "d2water MEAN", "")

# Process: Join Field
arcpy.JoinField_management(sites_morans_Ar_Merge__3_, "d2h2o", f_value_, "FREQUENCY", "FREQUENCY")

#step 13: 
# Import arcpy module
import arcpy


# Local variables:
d2h2od2avkat_sitepoints = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\d2h2od2avkat_sitepoints"
cum_viewshed_final = "C:\\datatemp\\cum_viewshed.gdb\\cum_viewshed_final"
exposure_sitepoints = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\exposure_sitepoints"
exposure_sitepoints__2_ = exposure_sitepoints
exposure_sitepoints__4_ = exposure_sitepoints__2_
exposure_sitepoints__3_ = exposure_sitepoints__4_
allceram_krnl = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\allceram_krnl"
density_sitepoints = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\density_sitepoints"
density_sitepoints__2_ = density_sitepoints
density_sitepoints__4_ = density_sitepoints__2_
density_sitepoints__3_ = density_sitepoints__4_
Avkat_DBO_dem_quickbird_extent = "Avkat.DBO.dem_quickbird_extent"
slope__2_ = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\slope"
slope_sitepoints = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\slope_sitepoints"
slope_sitepoints__2_ = slope_sitepoints
slope_sitepoints__3_ = slope_sitepoints__2_
slope_sitepoints__4_ = slope_sitepoints__3_
excel = "O:\\cross_regional\\data\\databases\\excel"
excel__3_ = excel
sample_points = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\sample_points"
exposure_samplepoints = "O:\\cross_regional\\data\\databases\\functional_model.gdb\\exposure_samplepoints"
exposure_samplepoints__2_ = exposure_samplepoints
exposure_samplepoints__3_ = exposure_samplepoints__2_
exposure_samplepoints__4_ = exposure_samplepoints__3_

# Process: Extract Values to Points
arcpy.gp.ExtractValuesToPoints_sa(d2h2od2avkat_sitepoints, cum_viewshed_final, exposure_sitepoints, "NONE", "VALUE_ONLY")

# Process: Add Field
arcpy.AddField_management(exposure_sitepoints, "exposure", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field
arcpy.CalculateField_management(exposure_sitepoints__2_, "exposure", "[RASTERVALU]", "VB", "")

# Process: Delete Field
arcpy.DeleteField_management(exposure_sitepoints__4_, "Join_Count;TARGET_FID;JOIN_FID;Id;d2water;d2avkat;RASTERVALU")

# Process: Extract Values to Points (3)
arcpy.gp.ExtractValuesToPoints_sa(d2h2od2avkat_sitepoints, allceram_krnl, density_sitepoints, "INTERPOLATE", "VALUE_ONLY")

# Process: Add Field (2)
arcpy.AddField_management(density_sitepoints, "density", "DOUBLE", "12", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field (2)
arcpy.CalculateField_management(density_sitepoints__2_, "density", "[RASTERVALU]", "VB", "")

# Process: Delete Field (2)
arcpy.DeleteField_management(density_sitepoints__4_, "Join_Count;TARGET_FID;JOIN_FID;Id;d2water;d2avkat;RASTERVALU")

# Process: Slope
arcpy.gp.Slope_sa(Avkat_DBO_dem_quickbird_extent, slope__2_, "DEGREE", "1")

# Process: Extract Values to Points (2)
arcpy.gp.ExtractValuesToPoints_sa(d2h2od2avkat_sitepoints, slope__2_, slope_sitepoints, "NONE", "VALUE_ONLY")

# Process: Add Field (3)
arcpy.AddField_management(slope_sitepoints, "slope", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field (3)
arcpy.CalculateField_management(slope_sitepoints__2_, "slope", "[RASTERVALU]", "VB", "")

# Process: Delete Field (3)
arcpy.DeleteField_management(slope_sitepoints__3_, "Join_Count;TARGET_FID;JOIN_FID;Id;OP;SU;d2water;d2avkat;RASTERVALU")

# Process: Table to dBASE (multiple)
arcpy.TableToDBASE_conversion("O:\\cross_regional\\data\\databases\\functional_model.gdb\\exposure_sitepoints;O:\\cross_regional\\data\\databases\\functional_model.gdb\\density_sitepoints;O:\\cross_regional\\data\\databases\\functional_model.gdb\\slope_sitepoints", excel)

# Process: Extract Values to Points (4)
arcpy.gp.ExtractValuesToPoints_sa(sample_points, cum_viewshed_final, exposure_samplepoints, "NONE", "VALUE_ONLY")

# Process: Add Field (4)
arcpy.AddField_management(exposure_samplepoints, "exposure", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field (4)
arcpy.CalculateField_management(exposure_samplepoints__2_, "exposure", "[RASTERVALU]", "VB", "")

# Process: Delete Field (4)
arcpy.DeleteField_management(exposure_samplepoints__3_, "RASTERVALU")




