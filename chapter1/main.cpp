#include "Triangle.hpp"
#include "rasterizer.hpp"
#include <eigen3/Eigen/Eigen>
#include <iostream>
#include <opencv2/opencv.hpp>

constexpr double MY_PI = 3.1415926;

Eigen::Matrix4f get_view_matrix(Eigen::Vector3f eye_pos)
{
    Eigen::Matrix4f view = Eigen::Matrix4f::Identity();

    Eigen::Matrix4f translate;
    translate << 1, 0, 0, -eye_pos[0], 0, 1, 0, -eye_pos[1], 0, 0, 1,
        -eye_pos[2], 0, 0, 0, 1;

    view = translate * view;

    return view;
}
Eigen::Matrix4f get_rotation_model_matrix(Eigen::Vector3f axis,float rotation_angle)
{
    Eigen::Matrix4f rotationModel;
    const double pi = acos(-1.0);
    float thea = rotation_angle*pi/180;
    Eigen::Matrix3f tmp0;
    float x = axis[0];
    float y = axis[1];
    float z = axis[2];
    tmp0<< 0,-z,y,z,0,-x,-y,x,0;
    Eigen::Matrix3f tmp = (1-cos(thea))*axis*axis.transpose() + cos(thea)*Eigen::Matrix3f::Identity()
    +sin(thea)*tmp0;
    rotationModel<< tmp(0,0),tmp(0,1),tmp(0,2),0,tmp(1,0),tmp(1,1),tmp(1,2),0,tmp(2,0),tmp(2,1),tmp(2,2),0,0,0,0,1;
    return rotationModel;
}



Eigen::Matrix4f get_model_matrix(float rotation_angle)
{
    // Eigen::Matrix4f model = Eigen::Matrix4f::Identity();

    // // TODO: Implement this function
    // // Create the model matrix for rotating the triangle around the Z axis.
    // // Then return it.
    // Eigen::Matrix4f translate;
    // const double pi = acos(-1.0);
    // float c = cos(rotation_angle*pi/180);
    // float s = sin(rotation_angle*pi/180);
    // translate << c, -s, 0, 0, s, c, 0, 0, 0, 0, 1,
    //     0, 0, 0, 0, 1;

    // return translate*model;
    Eigen::Vector3f axis;
    axis<<0.3,0.4,0.5;
    return get_rotation_model_matrix(axis,rotation_angle);
}





Eigen::Matrix4f get_projection_matrix(float eye_fov, float aspect_ratio,
                                      float zNear, float zFar)
{
    // Students will implement this function

    Eigen::Matrix4f projection ;

    // TODO: Implement this function
    // Create the projection matrix for the given parameters.
    // Then return it.
    float n = zNear;
    float f = zFar;
    const double pi = acos(-1.0);
    float t =  (-n)*tan(eye_fov*pi/180/2);
    float r = t/aspect_ratio;
    projection << n/r,0,0,0,0,n/t,0,0,0,0,(f+n)/(f-n),2*f*n/(f-n),0,0,1,0;
    return projection;
}

int main(int argc, const char** argv)
{
    float angle = 0;
    bool command_line = false;
    std::string filename = "output.png";

    if (argc >= 3) {
        command_line = true;
        angle = std::stof(argv[2]); // -r by default
        if (argc == 4) {
            filename = std::string(argv[3]);
        }
        else
            return 0;
    }

    rst::rasterizer r(700, 700);

    Eigen::Vector3f eye_pos = {0, 0, 5};

    std::vector<Eigen::Vector3f> pos{{2, 0, -2}, {0, 2, -2}, {-2, 0, -2}};

    std::vector<Eigen::Vector3i> ind{{0, 1, 2}};

    auto pos_id = r.load_positions(pos);
    auto ind_id = r.load_indices(ind);

    int key = 0;
    int frame_count = 0;

    if (command_line) {
        r.clear(rst::Buffers::Color | rst::Buffers::Depth);

        r.set_model(get_model_matrix(angle));
        r.set_view(get_view_matrix(eye_pos));
        r.set_projection(get_projection_matrix(45, 1, 0.1, 50));

        r.draw(pos_id, ind_id, rst::Primitive::Triangle);
        cv::Mat image(700, 700, CV_32FC3, r.frame_buffer().data());
        image.convertTo(image, CV_8UC3, 1.0f);

        cv::imwrite(filename, image);

        return 0;
    }

    while (key != 27) {
        r.clear(rst::Buffers::Color | rst::Buffers::Depth);

        r.set_model(get_model_matrix(angle));
        r.set_view(get_view_matrix(eye_pos));
        r.set_projection(get_projection_matrix(45, 1, 0.1, 50));

        r.draw(pos_id, ind_id, rst::Primitive::Triangle);

        cv::Mat image(700, 700, CV_32FC3, r.frame_buffer().data());
        image.convertTo(image, CV_8UC3, 1.0f);
        cv::imshow("image", image);
        key = cv::waitKey(10);

        std::cout << "frame count: " << frame_count++ << '\n';

        if (key == 'a') {
            angle += 10;
        }
        else if (key == 'd') {
            angle -= 10;
        }
    }

    return 0;
}
