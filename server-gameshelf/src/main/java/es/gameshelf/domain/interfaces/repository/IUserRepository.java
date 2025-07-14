package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Role;
import es.gameshelf.domain.User;
import es.gameshelf.domain.WishListItem;

import java.util.List;
import java.util.Map;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IUserRepository {
    User save(User user);
    List<User> findAll();
    List<WishListItem> findAllByRole(Role role);
    Map<Role, Integer> countAllGroupedByRole();
    User findById(Integer id);
    User findByUsername(String username);
    User findByEmail(String email);
    boolean delete(Integer id);
    User update(User user);
    User updatePassword(User user);
    User updateUsername(User user);
    User updateEmail(User user);
    User updatePicture(User user);
    User updateRole(User user);
    User verify(User user);

}
