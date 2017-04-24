#include <vigir_footstep_planning_default_plugins/world_model/terrain_model_uneven.h>

#include <pcl_conversions/pcl_conversions.h>

#include <pcl/io/pcd_io.h>
#include <pcl/kdtree/kdtree_flann.h>

#include <vigir_footstep_planning_lib/helper.h>
#include <vigir_footstep_planning_lib/math.h>

#include <vigir_terrain_classifier/terrain_model.h>

//#include "../uneven_terrain_stand/uneven_terrain_stand.h"
//#include "../uneven_terrain_stand/foot_state_uneven.h"
#include <vigir_footstep_planning_default_plugins/uneven_terrain_stand/uneven_terrain_stand.h>
#include <vigir_footstep_planning_default_plugins/uneven_terrain_stand/foot_state_uneven.h>

namespace vigir_footstep_planning
{
TerrainModelUneven::TerrainModelUneven(const std::string& name)
  : TerrainModel(name)
{
	// TODO load as ROS parameter in the node
	myPred = new MyPredict();
	myPred->init("../catkin_ws/src/vigir_footstep_planning_core/vigir_footstep_planning_default_plugins/src/uneven_terrain_stand/frozen_model_three_points.pb");
}

bool TerrainModelUneven::update3DData(geometry_msgs::Pose& p) const
{
  return terrain_model->update3DData(p);
}

bool TerrainModelUneven::update3DData(State& s) const {

	bool result = true;

	// get z
	double z = s.getZ();
	if (!getHeight(s.getX(), s.getY(), z)) {
		result = false;
	} else {
		s.setZ(z);
	}

	FootForm footForm = FootForm();

	// calculate the foot stand (including the normal and support, contact points, point set, etc)
	FootStateUneven footStand;
	try{

		UnevenTerrainStand unevenStand = UnevenTerrainStand(s, foot_size, terrain_model->getHeightGridMap(), footForm, myPred);
		footStand = unevenStand.getStand();
		std::vector<double> n = footStand.getNormal();

		s.setFootStateUneven(footStand);			// store for later use, e.g. visualizations
		s.setGroundContactSupport(footStand.getSupport());
		s.setNormal(n[0], n[1], n[2]);
		//s.setZ(footStand.height);

	}catch(std::exception const & ex){
		// TODO might throw exception if ill formed stand is calculated (bad point set to calculate hull)
		//ROS_INFO("Bad stand.");
		result = false;
	}

	if(footStand.getValid() != 1) {
		result = false;
	}

	// make sure that the pose does not contain NANs
	tf::Vector3 orig = s.getPose().getOrigin();
	for(int i = 0; i < 4; i++) {
	  if(std::isnan(orig.m_floats[i])) {
		  result = false;
	  }
	}

	// TODO maybe future work
	// TODO smooth each point with surroundings bc sensitive to noise
	// TODO too much normals turn out to be 0
	// TODO is normal pointing up or down?
	// TODO future work TODO could select ZMP to choose best support

	return result;
}

}

#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(vigir_footstep_planning::TerrainModelUneven, vigir_footstep_planning::TerrainModelPlugin)
