import pyautogui as pyg
import random
import numpy as np
import json
import os
import time

class UnityEyesDataCreator:

    def __init__(self, datatype, ids=300, frames_per_id=40):
        self.datatype = datatype
        self.face_position = 0
        self.id_count = 0
        self.image_count = 0
        self.velocity = np.asarray([random.randint(0, 5), random.randint(0, 5)])
        self.moment = np.asarray([random.randint(0, 2), random.randint(0, 2)])
        # self.mouse_location = None #self.find_center()
        self.center = None # self.find_center()
        # self.command_lclick_eyes_at_loc(self.mouse_location)
        self.frames_per_id = frames_per_id
        self.unity_path = "C:\\work\\UnityEyes_Windows"
        self._center_guess = [500, 500]
        self._x_correction = 0
        self._y_correction = 0

    def get_looking_vec_json(self, json_path):
        """

        :param json_path:
        :return:
        """
        data_file = open(json_path)
        data = json.load(data_file)
        look_vec = list(eval(data['eye_details']['look_vec']))
        return look_vec

    def get_first_json_path(self):
        return os.path.join(self.unity_path, "imgs", "1.json")

    def command_lclick_eyes_at_rel(self, relative_distance):
        pyg.moveRel(relative_distance[0], relative_distance[1], duration=0)
        pyg.click(button='middle')

    def command_click_eyes_at_loc(self, location):
        pyg.middleClick(location[0], location[1]) #, button='middle')

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
    def get_current_looking_vec(self):
        self.command_save_image()
        time.sleep(0.01)
        current_looking_vec = self.get_looking_vec_json(self.get_first_json_path())
        os.remove(self.get_first_json_path())
        return current_looking_vec
    def command_save_image(self):
        """
        save image at location
        """
        pyg.typewrite("s")

    def find_center(self):
        """
        turn eye to face camera. the look vec is positive when the eye looks to the right and upwards
        :return:
        """
        for step_size in [1, 0.1, 0.01, 0.001, 0.0001, 0.00001]:
            x_looping = False
            while True:
                self.command_click_eyes_at_loc(self._center_guess)
                current_look_vec = self.get_current_looking_vec()
                x_look_vec = current_look_vec[0]
                y_look_vec = current_look_vec[1]
                if x_look_vec == y_look_vec == 0:
                    self.center = self._center_guess
                    return self.center
                else:
                    if x_look_vec > 0:
                        if self._x_correction == 1:
                            # reduce step size
                            x_looping = True
                            # break

                        self._x_correction = -1
                    else:
                        if self._x_correction == -1:
                            # reduce step size
                            x_looping = True
                            # break
                        self._x_correction = 1

                    if y_look_vec > 0:
                        if self._y_correction == 1:
                            # reduce step size
                            if x_looping:
                                break
                        self._y_correction = -1
                    else:
                        if self._y_correction == -1:
                            # reduce step size
                            if x_looping:
                                break
                        self._y_correction = 1

                    self._center_guess = [self._center_guess[0] + self._x_correction * step_size,
                                          self._center_guess[1] + self._y_correction * step_size]
                    print(f"Guess {self._center_guess}")


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
        face_dict = {'center': 5, 'left': 4, 'right': 6, "bottom": 2, "top": 8}
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
            for frame_idx in range(self.frames_per_id):
                self.move_eyes()
                self.collect_image()

    def give_time_to_open_unity(self, sec=7):
        for s in range(sec,0, -1):
            print(f"Data collection will start in {s} seconds, open unity in the foreground")
            # pyg.click(500+s, 500+s, button='MIDDLE')
            time.sleep(1)

    def displayMousePosition(self):
        while True:
            time.sleep(0.2)
            pyg.displayMousePosition()

if __name__ == "__main__":
    dataset_creator = UnityEyesDataCreator(datatype="temporal", ids=1, frames_per_id=10)
    dataset_creator.give_time_to_open_unity(4)
    dataset_creator.find_center()
    dataset_creator.displayMousePosition()