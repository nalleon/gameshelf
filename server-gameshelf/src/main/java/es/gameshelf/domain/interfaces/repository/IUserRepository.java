package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.User;

import java.util.List;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IUserRepository {
    User save(User user);
    List<User> findAll();
    User findById(Integer id);
    User findByUsername(String username);
    User findByEmail(String email);
    boolean delete(Integer id);
    User update(User user);
    User updatePassword(User user);
    User updateUsername(User user);
    User updateEmail(User user);
    User updatePicture(User user);
}
