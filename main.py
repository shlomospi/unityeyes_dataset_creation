import pyautogui as pyg
import random
import numpy as np
import json
import os


class UnityEyesDataCreator:

    def __init__(self, datatype, ids=300, frames_per_id=40):
        self.datatype = datatype
        self.face_position = 0
        self.id_count = 0
        self.image_count = 0
        self.velocity = np.asarray([random.randint(0, 5), random.randint(0, 5)])
        self.moment = np.asarray([random.randint(0, 2), random.randint(0, 2)])
        self.mouse_location = self.find_center()
        self.center = self.find_center()
        self.command_lclick_eyes_at_loc(self.mouse_location)
        self.frames_per_id = frames_per_id
        self.unity_path = "C:\work\UnityEyes_Windows"

    def get_looking_vec_json(self, json_path):
        """

        :param json_path:
        :return:
        """
        data_file = open(json_path)
        data = json.load(data_file)
        look_vec = list(eval(data['eye_details']['look_vec']))
        return look_vec

    def get_first_json(self):
        return os.path.join(self.unity_path, "imgs", "1.json")


    def command_lclick_eyes_at_rel(self, relative_distance):
        pyg.moveRel(relative_distance[0], relative_distance[1], duration=0)
        pyg.click(button='middle')

    def command_lclick_eyes_at_loc(self, location):
        pyg.click(location[0], location[1], button='middle')

    def command_randomize_id(self):
        """
        randomize id
        """
        self.id_count += 1
        pyg.typewrite("r")

    def command_toggle_ui(self):
        """
        toggle UI display
        """
        pyg.typewrite("h")

    def command_randomize_illumination(self):
        """
        randomize illumination
        """
        pyg.typewrite("l")

    def command_save_image(self):
        """
        save image at location
        """
        pyg.typewrite("s")

    def find_center(self):
        '''
        turn eye to face camera. the look vec is positive when the eye looks to the right and upwards
        :return:
        '''
        print("TODO find center")
        for step_size in [10,1,0.1,0.01,0.001,0.0001,0.00001]:
            while True:

                current_look_vec = self.get_looking_vec_json(self.get_first_json())
                x_look_vec = current_look_vec[0]
                y_look_vec = current_look_vec[1]
                if x_look_vec == y_look_vec == 0:
                    return True
                if x_look_vec > 0:

        center_guess = [500, 500]

    def get_last_image_gaze_angle(self):
        pass

    def change_id(self):
        """
        randomize id and illumination
        """

        self.command_randomize_illumination()
        self.command_randomize_id()

    def collect_image(self):
        """
        save_image and progress image count
        """
        self.command_save_image()
        self.process_image()
        self.image_count += 1

    def process_image(self):
        """
        catch last created image and prepare a cutout of the image with a meaningful name
        """
        name_template = "ID{0:04d}_P{0:02d}_T{0:02d}_N{0:02d}_F{0:05d}_V{:4.2f}_H{:4.2f}.bmp"
        image_name = name_template.format(self.id_count, )
        # take last saved image
        # cut it
        # give it the name and save it

    def progress_eye_flow(self):
        """
        progress eye flow
        """
        self.mouse_location += self.velocity + 0.5 * [self.moment[0] ** 2, self.moment[1] ** 2]
        self.velocity += self.moment
        self.moment += np.asarray([random.randint(-1, 1), random.randint(-1, 1)])

    def move_eyes(self):
        if self.datatype == 'clip':
            self.progress_eye_flow()

    def determine_face_position(self, face_position):
        """
        return and int that indicates the face position
        :param face_position:
        :return:
        """
        assert face_position in ['center', 'left']
        face_dict = {'center': 5, 'left': 4, 'right': 6, "bottom": 2, "top":8}
        return face_dict[face_position]

    def collect_dataset(self, face_position, ids, frames_per_id=40):
        """
        Main function to create dataset
        :param face_position:
        :param ids:
        :param frames_per_id:
        :return:
        """
        # get face position identification int
        self.face_position = self.determine_face_position(face_position)
        for id_idx in ids:
            self.change_id()
            for frame_idx in self.frames_per_id:
                self.move_eyes()
                self.collect_image()


