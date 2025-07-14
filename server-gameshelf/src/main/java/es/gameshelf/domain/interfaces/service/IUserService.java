package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.*;

import java.util.List;
import java.util.Map;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IUserService {
    User add(String username, String email, String password);
    List<User> findAll();
    List<WishListItem> findAllByRole(Role role);
    Map<Role, Integer> countAllGroupedByRole();
    User findById(Integer id);
    User findByUsername(String username);
    User findByEmail(String email);
    boolean delete(Integer id);
    User update(Integer id, String username, String email, String password, String profilePictureRole, Role role);
    User updatePassword(Integer id, String password);
    User updateUsername(Integer id, String username);
    User updateEmail(Integer id, String email);
    User updatePicture(Integer id, String profilePicture);
    User updateRole(Integer id, Role role);
    User verify(Integer id);

}
