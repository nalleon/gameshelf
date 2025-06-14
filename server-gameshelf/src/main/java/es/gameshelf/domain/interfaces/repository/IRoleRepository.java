package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Role;

import java.util.List;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IRoleRepository {
    Role save(Role role);
    List<Role> findAll();
    Role findById(Integer id);
    Role findByName(String name);
    boolean delete(Integer id);
    Role update(Role role);
}
