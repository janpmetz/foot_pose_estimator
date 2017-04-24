#include <vigir_footstep_planning_msgs/visualization.h>



namespace vigir_footstep_planning
{
namespace msgs
{
void footToFootMarker(const Foot& foot, const geometry_msgs::Vector3& foot_size, const std_msgs::ColorRGBA& color, visualization_msgs::Marker& marker)
{
  marker.header = foot.header;
  marker.ns = "vigir_footstep_planning/step_plan";
  marker.type = visualization_msgs::Marker::CUBE;
  marker.action = visualization_msgs::Marker::ADD;

  marker.pose = foot.pose;
  marker.pose.position.z += 0.5*foot_size.z;
  marker.scale = foot_size;

  marker.color = color;


  marker.lifetime = ros::Duration();
}

void feetToFootMarkerArray(const Feet& feet, const geometry_msgs::Vector3& foot_size, const std_msgs::ColorRGBA& color, visualization_msgs::MarkerArray& marker_array)
{
  visualization_msgs::Marker marker;
  marker_array.markers.clear();

  footToFootMarker(feet.left, foot_size, color, marker);
  marker_array.markers.push_back(marker);
  marker.id++;

  footToFootMarker(feet.right, foot_size, color, marker);
  marker_array.markers.push_back(marker);
}

void stepToFootMarker(const Step& step, const geometry_msgs::Vector3& foot_size, const std_msgs::ColorRGBA& color, visualization_msgs::Marker& marker)
{
  footToFootMarker(step.foot, foot_size, color, marker);
}

void nonConvexFootMarkers(const Step& step, const geometry_msgs::Vector3& foot_size, const std_msgs::ColorRGBA& color, visualization_msgs::Marker& marker, visualization_msgs::MarkerArray& marker_array)
{

		if(step.valid_uneven != 1) {
			return;
		}

		std::vector<double> p1 = step.p1;
		std::vector<double> p2 = step.p2;
		std::vector<double> p3 = step.p3;
		std::vector<double> normal = step.normal;

		ROS_INFO("VECTOR SIZE: %d ", p1.size());
		if(p1.size() == 0){
			return;
		}

		// assemble the point map again
		std::map<int, std::vector<double>> original_point_map;
		for(int i = 0; i < step.original_point_map_keys.size(); i++) {
			std::vector<double> v = {step.original_point_map_x[i], step.original_point_map_y[i], step.original_point_map_z[i]};
			original_point_map[step.original_point_map_keys[i]] = v;
		}

		//axis-angle rotation
		tf::Vector3 axis(normal[0],normal[1],normal[2]);
		tf::Vector3 marker_axis(1, 0, 0);
		tf::Quaternion qt(marker_axis.cross(axis.normalize()), marker_axis.angle(axis.normalize()));
		geometry_msgs::Quaternion quat_msg;
		tf::quaternionTFToMsg(qt, quat_msg);


		// 3 contact points
		visualization_msgs::Marker marker1;
		marker1.id = marker.id;
		marker1.header = step.foot.header;
		//marker.header.stamp = ros::Time();
		marker1.type = visualization_msgs::Marker::POINTS;
		marker1.action = visualization_msgs::Marker::ADD;
		marker1.scale.x = 0.02;
		marker1.scale.y = 0.02;
		marker1.scale.z = 0.02;
		marker1.color.a = 1.0;
		marker1.color.r = 0.0;
		marker1.color.g = 1.0;
		marker1.color.b = 0.0;
		marker1.ns = "vigir_footstep_planning/step_plan";

		geometry_msgs::Point p_1;
		geometry_msgs::Point p_2;
		geometry_msgs::Point p_3;

		p_1.x = p1[0];
		p_1.y = p1[1];
		p_1.z = p1[2];

		p_2.x = p2[0];
		p_2.y = p2[1];
		p_2.z = p2[2];

		p_3.x = p3[0];
		p_3.y = p3[1];
		p_3.z = p3[2];

		std::vector<geometry_msgs::Point> my_points;
		my_points.push_back(p_1);
		my_points.push_back(p_2);
		my_points.push_back(p_3);

		for (int ii = 0; ii < my_points.size(); ++ii)
		{
		    std_msgs::ColorRGBA c;
		    	c.r = 1.0;
		    c.a = 1;

		    marker1.points.push_back(my_points[ii]);
		    // Here, the field colors is populated with a specific color per point.
		    marker1.colors.push_back(c);
		}

	    marker_array.markers.push_back(marker1);
	    marker.id++;

		// 3 contact points TRIANGLE
	    visualization_msgs::Marker marker4;
		marker4.id = marker.id;
		marker4.ns = "vigir_footstep_planning/step_plan";
		marker4.header = step.foot.header;
		marker4.type = visualization_msgs::Marker::TRIANGLE_LIST;
		marker4.action = visualization_msgs::Marker::ADD;

		marker4.scale.x = 0.01;
		marker4.scale.y = 0.01;
		marker4.scale.z = 0.01;
		marker4.color.a = 1.0;
		marker4.color.r = 1.0;
		marker4.color.g = 0.0;
		marker4.color.b = 0.0;

		marker4.points.push_back(p_1);
		marker4.points.push_back(p_2);
		marker4.points.push_back(p_3);

		std_msgs::ColorRGBA c;
		c.r = 0;
		c.g = 1;
		c.b = 0;

		marker4.colors.push_back(c);
		marker4.colors.push_back(c);
		marker4.colors.push_back(c);


	    marker_array.markers.push_back(marker4);
	    marker.id++;

		// arrow
		visualization_msgs::Marker marker2;
		marker2.id = marker.id;
		marker2.header = step.foot.header;
	    //arrow.header.stamp = ros::Time::now();
		marker2.ns = "vigir_footstep_planning/step_plan";

		marker2.type = visualization_msgs::Marker::ARROW;
		marker2.action = visualization_msgs::Marker::ADD;

		geometry_msgs::Point pos;
		pos.x = p1[0];
		pos.y = p1[1];
		pos.z = p1[2];
		marker2.pose.position = pos;
		marker2.pose.orientation = quat_msg;

		marker2.scale.x=0.1;
		marker2.scale.y=0.01;
		marker2.scale.z = 0.01;

		marker2.color.g = 1.0f;
		marker2.color.a = 1.0;
		marker2.color.r = 0.0f;
		marker2.color.b = 0.0f;

	    marker_array.markers.push_back(marker2);
	    marker.id++;
	    // arrow



		// foot points
		visualization_msgs::Marker marker3;
		marker3.id = marker.id;

		marker3.header = step.foot.header;
		//foot.header.stamp = ros::Time();
		marker3.type = visualization_msgs::Marker::POINTS;
		marker3.action = visualization_msgs::Marker::ADD;
		marker3.scale.x = 0.01;
		marker3.scale.y = 0.01;
		marker3.scale.z = 0.01;
		marker3.color.a = 1.0;
		marker3.color.r = 1.0;
		marker3.color.g = 0.0;
		marker3.color.b = 0.0;

		marker3.ns = "vigir_footstep_planning/step_plan";

		for (std::map<int, std::vector<double>>::iterator iter = original_point_map.begin();
		                                        iter != original_point_map.end();
		                                        ++iter){
			std::vector<double> original_point = iter->second;


		    geometry_msgs::Point p;
			p.x = original_point[0];
			p.y = original_point[1];
			p.z = original_point[2];

			std_msgs::ColorRGBA c;

			c.g = 1.0;
			c.a = 1;

			marker3.points.push_back(p);
			// Here, the field colors is populated with a specific color per point.
			marker3.colors.push_back(c);
		}

	    marker_array.markers.push_back(marker3);

		return;

}

void stepPlanToFootMarkerArray(const std::vector<Step>& steps, const geometry_msgs::Vector3& foot_size, visualization_msgs::MarkerArray& marker_array, bool add_step_index)
{
  std_msgs::ColorRGBA color;
  color.r = 0.0;
  color.g = 0.0;
  color.b = 0.0;
  color.a = 0.6;

  visualization_msgs::Marker marker;

  marker_array.markers.clear();

  for (std::vector<Step>::const_iterator itr = steps.begin(); itr != steps.end(); itr++)
  {
    // colorize
    color.r = itr->foot.foot_index == Foot::LEFT ? 1.0 : 0.0;
    color.g = itr->foot.foot_index == Foot::LEFT ? 0.0 : 1.0;


    // transform
    if((*itr).valid_uneven) {
        nonConvexFootMarkers(*itr, foot_size, color, marker, marker_array);
		marker.id++;
    } else {
    	stepToFootMarker(*itr, foot_size, color, marker);
		marker_array.markers.push_back(marker);
		marker.id++;
    }

//
//    // add text
//    if (add_step_index)
//    {
//      marker.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
//      marker.action = visualization_msgs::Marker::ADD;
//      marker.text = boost::lexical_cast<std::string>(itr->step_index);
//      marker.scale.z *= 3;
//      marker.color.r = 1.0;
//      marker.color.g = 1.0;
//      marker.color.b = 1.0;
//      marker.color.a = 0.7;
//
//      marker_array.markers.push_back(marker);
//      marker.id++;
//    }

  }
}

void stepPlanToFootMarkerArray(const StepPlan& step_plan, const geometry_msgs::Vector3& foot_size, visualization_msgs::MarkerArray& marker_array, bool add_step_index)
{
  stepPlanToFootMarkerArray(step_plan.steps, foot_size, marker_array, add_step_index);
}

void feetToUpperBodyMarker(const Feet& feet, const geometry_msgs::Vector3& upper_body_size, const geometry_msgs::Vector3& upper_body_origin_shift, const std_msgs::ColorRGBA& color, visualization_msgs::Marker& marker, bool flat)
{
  marker.header = feet.header;
  marker.ns = "vigir_footstep_planning/upper_body";
  marker.type = visualization_msgs::Marker::CUBE;
  marker.action = visualization_msgs::Marker::ADD;

  // approximate upper body position
  marker.pose.position.x = 0.5 * (feet.left.pose.position.x + feet.right.pose.position.x);
  marker.pose.position.y = 0.5 * (feet.left.pose.position.y + feet.right.pose.position.y);
  marker.pose.position.z = 0.5 * (feet.left.pose.position.z + feet.right.pose.position.z);
  marker.pose.orientation = tf::createQuaternionMsgFromYaw(0.5 * (tf::getYaw(feet.left.pose.orientation) + tf::getYaw(feet.right.pose.orientation)));

  // determine shift of polygon based on orientation
  tf::Transform transform;
  tf::poseMsgToTF(marker.pose, transform);
  tf::Vector3 shifted;
  tf::vector3MsgToTF(upper_body_origin_shift, shifted);
  shifted = transform * shifted;

  marker.pose.position.x = shifted.getX();
  marker.pose.position.y = shifted.getY();
  marker.pose.position.z = shifted.getZ();

  // finalize marker
  marker.pose.position.z += flat ? 0.01 : 0.5*upper_body_size.z;
  marker.scale = upper_body_size;
  if (flat)
    marker.scale.z = 0.02;
  marker.color = color;

  marker.lifetime = ros::Duration();
}

void stepPlanToUpperBodyMarkerArray(const std::vector<Step>& steps, const geometry_msgs::Vector3& upper_body_size, const geometry_msgs::Vector3& upper_body_origin_shift, visualization_msgs::MarkerArray& marker_array, bool add_step_index)
{
  std_msgs::ColorRGBA color;
  color.r = 0.0;
  color.g = 0.0;
  color.b = 0.4;
  color.a = 0.2;

  visualization_msgs::Marker marker;

  marker_array.markers.clear();

  Feet feet;
  for (std::vector<Step>::const_iterator itr = steps.begin(); itr != steps.end(); itr++)
  {
    const Step& step = *itr;
    if (step.foot.foot_index == Foot::LEFT)
      feet.left = step.foot;
    else
      feet.right = step.foot;

    if (itr == steps.begin())
    {
      feet.header = step.header;
      continue;
    }

    // transform
    feetToUpperBodyMarker(feet, upper_body_size, upper_body_origin_shift, color, marker);
    marker_array.markers.push_back(marker);
    marker.id++;

    // add text
    if (add_step_index)
    {
      marker.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
      marker.action = visualization_msgs::Marker::ADD;
      marker.text = boost::lexical_cast<std::string>(itr->step_index);
      marker.scale.z *= 0.1;
      marker.color.r = 1.0;
      marker.color.g = 1.0;
      marker.color.b = 1.0;
      marker.color.a = 0.7;

      marker_array.markers.push_back(marker);
      marker.id++;
    }
  }
}

void stepPlanToUpperBodyMarkerArray(const StepPlan& step_plan, const geometry_msgs::Vector3& upper_body_size, const geometry_msgs::Vector3& upper_body_origin_shift, visualization_msgs::MarkerArray& marker_array, bool add_step_index)
{
  stepPlanToUpperBodyMarkerArray(step_plan.steps, upper_body_size, upper_body_origin_shift, marker_array, add_step_index);
}

void stepPlanToPath(const StepPlan& step_plan, nav_msgs::Path& path)
{
  path.poses.clear();

  path.header = step_plan.header;
  for (std::vector<Step>::const_iterator itr = step_plan.steps.begin(); itr != step_plan.steps.end(); itr++)
  {
    geometry_msgs::PoseStamped pose;
    pose.header = step_plan.header;
    pose.pose = itr->foot.pose;
    path.poses.push_back(pose);
  }
}
}
}
